from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from conversation.models import Conversation
from conversation.api.schemas import ConversationDetailSerializer


class ConversationDetailView(generics.RetrieveAPIView):
    """
    View para recuperar detalhes de uma conversa específica, incluindo suas mensagens.
    """
    serializer_class = ConversationDetailSerializer
    lookup_field = 'conversation_id'

    def get_queryset(self):
        return Conversation.objects.all()

    def get_object(self):
        """
        Recupera o objeto baseado no UUID fornecido.
        Retorna 404 se a conversa não for encontrada.
        """
        try:
            return super().get_object()
        except Exception:
            raise NotFound(detail="Conversation not found")