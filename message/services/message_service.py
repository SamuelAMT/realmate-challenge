from django.db import transaction
from django.core.exceptions import ValidationError
from message.models import Message
from conversation.models import Conversation


class MessageService:
    """
    Serviço para operações relacionadas a mensagens.
    """

    @staticmethod
    def create_message(message_id, conversation_id, content, direction):
        """
        Cria uma nova mensagem na conversa especificada.

        Args:
            message_id (UUID): ID da mensagem
            conversation_id (UUID): ID da conversa
            content (str): Conteúdo da mensagem
            direction (str): Direção da mensagem (SENT ou RECEIVED)

        Returns:
            Message: Mensagem criada ou None se houver erro

        Raises:
            ValidationError: Se a mensagem não puder ser criada
        """
        if Message.objects.filter(id=message_id).exists():
            return None

        try:
            conversation = Conversation.objects.get(id=conversation_id)

            if not conversation.is_open:
                raise ValidationError(
                    "Cannot add message to closed conversation")

            # Cria a mensagem em caso da conversa estar aberta
            with transaction.atomic():
                message = Message(
                    id=message_id,
                    conversation=conversation,
                    content=content,
                    direction=direction
                )
                message.save()
                return message

        except Conversation.DoesNotExist:
            raise ValidationError("Conversation not found")