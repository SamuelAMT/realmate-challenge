from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from conversation.models import Conversation
from conversation.api.schemas.conversation import ConversationDetailSerializer


class ConversationDetailAPIView(generics.RetrieveAPIView):
    """
    API View para recuperar detalhes de uma conversa específica.
    GET /conversations/{conversation_id}/
    """
    serializer_class = ConversationDetailSerializer
    queryset = Conversation.objects.all()
    lookup_field = 'conversation_id'

    def get_object(self):
        """
        Sobrescreve o método get_object para lidar com UUIDs e erros de forma elegante
        """
        try:
            return super().get_object()
        except Exception as e:
            raise NotFound(detail="Conversation not found")
