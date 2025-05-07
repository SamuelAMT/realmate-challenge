from django.core.exceptions import ValidationError
from rest_framework import status
from conversation.services.conversation_service import ConversationService
from message.services.message_service import MessageService
from message.models import Message
import logging

logger = logging.getLogger(__name__)


class WebhookService:
    """
    Serviço para processamento de eventos de webhook.
    """

    def process_event(self, event_type, data, timestamp=None):
        """
        Processa um evento de webhook com base no seu tipo.

        Args:
            event_type (str): Tipo do evento (NEW_CONVERSATION, NEW_MESSAGE, CLOSE_CONVERSATION)
            data (dict): Dados do evento
            timestamp (str, optional): Timestamp do evento

        Returns:
            dict: Contém a resposta e o status HTTP
        """
        try:
            if event_type == 'NEW_CONVERSATION':
                return self._handle_new_conversation(data)
            elif event_type == 'NEW_MESSAGE':
                return self._handle_new_message(data)
            elif event_type == 'CLOSE_CONVERSATION':
                return self._handle_close_conversation(data)
            else:
                return {
                    "response": {
                        "error": f"Unsupported event type: {event_type}"},
                    "status": status.HTTP_400_BAD_REQUEST
                }
        except ValidationError as e:
            logger.error(f"Validation error in webhook processing: {str(e)}")
            return {
                "response": {"error": str(e)},
                "status": status.HTTP_400_BAD_REQUEST
            }
        except Exception as e:
            logger.exception(
                f"Unexpected error in webhook processing: {str(e)}")
            return {
                "response": {"error": "An unexpected error occurred"},
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }

    def _handle_new_conversation(self, data):
        """
        Processa o evento NEW_CONVERSATION.

        Args:
            data (dict): Dados do evento com o ID da conversa

        Returns:
            dict: Resposta e status HTTP
        """
        conversation_id = data.get('id')

        if not conversation_id:
            return {
                "response": {"error": "Missing conversation ID"},
                "status": status.HTTP_400_BAD_REQUEST
            }

        try:
            conversation = ConversationService.create_conversation(
                conversation_id)

            if not conversation:
                return {
                    "response": {"error": "Conversation already exists"},
                    "status": status.HTTP_409_CONFLICT
                }

            return {
                "response": {"message": "Conversation created",
                             "id": str(conversation.id)},
                "status": status.HTTP_201_CREATED
            }
        except ValueError:
            return {
                "response": {"error": "Invalid conversation ID format"},
                "status": status.HTTP_400_BAD_REQUEST
            }

    def _handle_new_message(self, data):
        """
        Processa o evento NEW_MESSAGE.

        Args:
            data (dict): Dados do evento com informações da mensagem

        Returns:
            dict: Resposta e status HTTP
        """
        message_id = data.get('id')
        direction = data.get('direction')
        content = data.get('content')
        conversation_id = data.get('conversation_id')

        # Validação dos campos obrigatórios
        if not all([message_id, direction, content, conversation_id]):
            return {
                "response": {"error": "Missing required message fields"},
                "status": status.HTTP_400_BAD_REQUEST
            }

        # Validação da direção
        if direction not in [Message.SENT, Message.RECEIVED]:
            return {
                "response": {
                    "error": f"Invalid message direction: {direction}"},
                "status": status.HTTP_400_BAD_REQUEST
            }

        try:
            try:
                message = MessageService.create_message(message_id,
                                                        conversation_id,
                                                        content, direction)

                if not message:
                    return {
                        "response": {"error": "Message already exists"},
                        "status": status.HTTP_409_CONFLICT
                    }

                return {
                    "response": {"message": "Message added",
                                 "id": str(message.id)},
                    "status": status.HTTP_201_CREATED
                }
            except ValidationError as e:
                if "Conversation not found" in str(e):
                    return {
                        "response": {"error": "Conversation not found"},
                        "status": status.HTTP_404_NOT_FOUND
                    }
                elif "closed conversation" in str(e).lower():
                    return {
                        "response": {
                            "error": "Cannot add message to closed conversation"},
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                else:
                    raise e
        except ValueError:
            return {
                "response": {"error": "Invalid UUID format"},
                "status": status.HTTP_400_BAD_REQUEST
            }

    def _handle_close_conversation(self, data):
        """
        Processa o evento CLOSE_CONVERSATION.

        Args:
            data (dict): Dados do evento com o ID da conversa

        Returns:
            dict: Resposta e status HTTP
        """
        conversation_id = data.get('id')

        if not conversation_id:
            return {
                "response": {"error": "Missing conversation ID"},
                "status": status.HTTP_400_BAD_REQUEST
            }

        try:
            conversation = ConversationService.close_conversation(
                conversation_id)

            if not conversation:
                return {
                    "response": {"error": "Conversation not found"},
                    "status": status.HTTP_404_NOT_FOUND
                }

            return {
                "response": {"message": "Conversation closed",
                             "id": str(conversation.id)},
                "status": status.HTTP_200_OK
            }
        except ValueError:
            return {
                "response": {"error": "Invalid conversation ID format"},
                "status": status.HTTP_400_BAD_REQUEST
            }
