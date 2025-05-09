from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from conversation.models import Conversation
from conversation.api.schemas.conversation import ConversationDetailSerializer


class ConversationDetailView(generics.RetrieveAPIView):
    """
    View para recuperar detalhes de uma conversa específica, incluindo suas mensagens.
    """
    serializer_class = ConversationDetailSerializer
    lookup_field = 'conversation_id'
    lookup_url_kwarg = 'conversation_id'

    @swagger_auto_schema(
        operation_summary="Recupera detalhes de uma conversa",
        operation_description="Retorna informações da conversa e suas mensagens",
        responses={
            200: ConversationDetailSerializer,
            404: "Conversa não encontrada"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        Recupera o objeto baseado no UUID fornecido.
        Retorna 404 se a conversa não for encontrada.
        """
        try:
            return super().get_object()
        except Exception:
            raise NotFound(detail="Conversation not found")
