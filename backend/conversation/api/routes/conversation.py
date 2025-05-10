from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from conversation.models import Conversation
from conversation.api.schemas.conversation import ConversationSerializer, \
    ConversationDetailSerializer


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for listing or retrieving conversations.
    """
    queryset = Conversation.objects.all()
    lookup_field = 'conversation_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationSerializer
        return ConversationDetailSerializer

    def get_object(self):
        """
        Override get_object to handle UUIDs and errors gracefully
        """
        try:
            return super().get_object()
        except Exception as e:
            raise NotFound(detail="Conversation not found")
