from django.db import transaction
from django.core.exceptions import ValidationError
import logging
import uuid

from conversation.models import Conversation
from message.models import Message

logger = logging.getLogger(__name__)


class WebhookService:
    """
    Serviço para processar webhooks recebidos.
    Manipula a lógica de negócio para diferentes tipos de eventos.
    """

    EVENT_NEW_CONVERSATION = "NEW_CONVERSATION"
    EVENT_NEW_MESSAGE = "NEW_MESSAGE"
    EVENT_CLOSE_CONVERSATION = "CLOSE_CONVERSATION"

    @classmethod
    def process_webhook(cls, webhook_data):
        """
        Processa o webhook com base no tipo de evento.

        Args:
            webhook_data (dict): Dados do webhook recebido

        Returns:
            dict: Resultado do processamento com chaves 'success' e 'message'

        Raises:
            ValidationError: Se os dados do webhook forem inválidos
        """
        if not webhook_data:
            raise ValidationError("Empty webhook data")

        event_type = webhook_data.get('type')
        data = webhook_data.get('data')

        if not event_type or not data:
            raise ValidationError(
                "Missing required webhook fields: type or data")

        # In case the API sends 'id' instead of 'conversation_id' for conversation events
        if event_type in [cls.EVENT_NEW_CONVERSATION,
                          cls.EVENT_CLOSE_CONVERSATION]:
            if 'id' in data and 'conversation_id' not in data:
                data['conversation_id'] = data['id']

            # For messages, map 'id' to 'message_id'
        if event_type == cls.EVENT_NEW_MESSAGE:
            if 'id' in data and 'message_id' not in data:
                data['message_id'] = data['id']

        # Roteamento do evento para o handler apropriado
        if event_type == cls.EVENT_NEW_CONVERSATION:
            return cls._handle_new_conversation(data)

        elif event_type == cls.EVENT_NEW_MESSAGE:
            return cls._handle_new_message(data)

        elif event_type == cls.EVENT_CLOSE_CONVERSATION:
            return cls._handle_close_conversation(data)

        else:
            raise ValidationError(f"Unsupported event type: {event_type}")

    @classmethod
    def _handle_new_conversation(cls, data):
        """
        Manipula evento de nova conversa.

        Args:
            data (dict): Dados do evento

        Returns:
            dict: Resultado do processamento
        """
        conversation_id = data.get('conversation_id')
        if not conversation_id:
            raise ValidationError("Missing conversation ID")

        try:
            conversation_id = uuid.UUID(conversation_id)
        except ValueError:
            raise ValidationError("Invalid conversation ID format")

        # Verifica se a conversa já existe
        if Conversation.objects.filter(conversation_id=conversation_id).exists():
            return {
                'success': False,
                'message': f"Conversation {conversation_id} already exists"
            }

        # Cria nova conversa
        with transaction.atomic():
            conversation = Conversation(conversation_id=conversation_id)
            conversation.save()

        return {
            'success': True,
            'message': f"Created new conversation with ID: {conversation_id}"
        }

    @classmethod
    def _handle_new_message(cls, data):
        """
        Manipula evento de nova mensagem.

        Args:
            data (dict): Dados do evento

        Returns:
            dict: Resultado do processamento
        """
        message_id = data.get('message_id')
        conversation_id = data.get('conversation_id')
        content = data.get('content')
        direction = data.get('direction')

        if not all([message_id, conversation_id, content, direction]):
            raise ValidationError("Missing required message fields")

        try:
            message_id = uuid.UUID(message_id)
            conversation_id = uuid.UUID(conversation_id)
        except ValueError:
            raise ValidationError("Invalid UUID format")

        # Validação da direção
        if direction not in [Message.SENT, Message.RECEIVED]:
            raise ValidationError(f"Invalid message direction: {direction}")

        # Verifica se a mensagem já existe
        if Message.objects.filter(message_id=message_id).exists():
            return {
                'success': False,
                'message': f"Message {message_id} already exists"
            }

        try:
            # Recupera a conversa
            conversation = Conversation.objects.get(conversation_id=conversation_id)

            if conversation.state == Conversation.CLOSED:
                return {
                    'success': False,
                    'message': f"Cannot add message to closed conversation {conversation_id}"
                }

            with transaction.atomic():
                message = Message(
                    message_id=message_id,
                    conversation=conversation,
                    content=content,
                    direction=direction
                )
                message.save()

            return {
                'success': True,
                'message': f"Added message {message_id} to conversation {conversation_id}"
            }

        except Conversation.DoesNotExist:
            return {
                'success': False,
                'message': f"Conversation {conversation_id} not found"
            }
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e)
            }

    @classmethod
    def _handle_close_conversation(cls, data):
        """
        Manipula evento de fechamento de conversa.

        Args:
            data (dict): Dados do evento

        Returns:
            dict: Resultado do processamento
        """
        conversation_id = data.get('conversation_id')
        if not conversation_id:
            raise ValidationError("Missing conversation ID")

        try:
            conversation_id = uuid.UUID(conversation_id)
        except ValueError:
            raise ValidationError("Invalid conversation ID format")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)

            if conversation.state == Conversation.CLOSED:
                return {
                    'success': False,
                    'message': f"Conversation {conversation_id} is already closed"
                }

            # Fecha a conversa
            with transaction.atomic():
                conversation.close()

            return {
                'success': True,
                'message': f"Closed conversation {conversation_id}"
            }

        except Conversation.DoesNotExist:
            return {
                'success': False,
                'message': f"Conversation {conversation_id} not found"
            }
