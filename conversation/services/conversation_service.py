from django.db import transaction
from conversation.models import Conversation


class ConversationService:
    """
    Serviço para operações relacionadas a conversas.
    """

    @staticmethod
    def create_conversation(conversation_id):
        """
        Cria uma nova conversa com o ID especificado.
        Retorna a conversa criada ou None se já existir.
        """
        if Conversation.objects.filter(id=conversation_id).exists():
            return None

        with transaction.atomic():
            conversation = Conversation(id=conversation_id)
            conversation.save()
            return conversation

    @staticmethod
    def close_conversation(conversation_id):
        """
        Fecha uma conversa existente.
        Retorna a conversa fechada ou None se não existir.
        """
        try:
            with transaction.atomic():
                conversation = Conversation.objects.get(id=conversation_id)
                if conversation.state == Conversation.CLOSED:
                    return conversation  # Já está fechada

                conversation.close()
                return conversation
        except Conversation.DoesNotExist:
            return None