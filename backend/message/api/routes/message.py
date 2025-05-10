from rest_framework import generics, status
from rest_framework.response import Response

from conversation.models import Conversation
from message.models import Message
from message.api.schemas.message import MessageSerializer


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    API View for listing and creating messages for a specific conversation.
    GET /api/conversations/{conversation_id}/messages/
    POST /api/conversations/{conversation_id}/messages/
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(
            conversation__conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
            serializer.save(conversation=conversation)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )
