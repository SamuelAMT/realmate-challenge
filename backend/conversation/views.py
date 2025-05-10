from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
import uuid
from conversation.models import Conversation
from conversation.api.schemas.conversation import (
    ConversationSerializer,
    ConversationDetailSerializer
)
from conversation.services.conversation_service import ConversationService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for listing, retrieving, and creating conversations.
    """
    queryset = Conversation.objects.all()
    lookup_field = 'conversation_id'

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return ConversationSerializer
        return ConversationDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a generated UUID.
        """
        try:
            conversation_id = uuid.uuid4()
            conversation = ConversationService.create_conversation(
                conversation_id)

            if conversation:
                serializer = self.get_serializer(conversation)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"status": "error",
                     "message": "Failed to create conversation"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self):
        """
        Override get_object to handle UUIDs and errors gracefully
        """
        try:
            return super().get_object()
        except Exception as e:
            raise NotFound(detail="Conversation not found")
