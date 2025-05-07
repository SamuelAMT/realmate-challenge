from django.db import models
import uuid


class Conversation(models.Model):
    """
    Representa uma conversa no sistema de atendimento.
    Uma conversa possui um estado (OPEN ou CLOSED) e pode conter múltiplas mensagens.
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    STATE_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=10, choices=STATE_CHOICES,
                             default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.state}"

    def close(self):
        """Fecha a conversa, alterando seu estado para CLOSED"""
        self.state = self.CLOSED
        self.save()

    @property
    def is_open(self):
        """Verifica se a conversa está aberta"""
        return self.state == self.OPEN

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'





# conversation/apps.py
from django.apps import AppConfig


class ConversationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversation'


# conversation/views.py
from django.shortcuts import get_object_or_404
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
    lookup_field = 'id'

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


# conversation/urls.py
from django.urls import path
from conversation.views import ConversationDetailView

urlpatterns = [
    path('<uuid:id>/', ConversationDetailView.as_view(),
         name='conversation-detail'),
]

# conversation/api/schemas.py
from rest_framework import serializers
from conversation.models import Conversation
from message.models import Message


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializador básico para o modelo Conversation.
    """

    class Meta:
        model = Conversation
        fields = ['id', 'state', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MessageInConversationSerializer(serializers.ModelSerializer):
    """
    Serializador para mensagens dentro do contexto de uma conversa.
    """

    class Meta:
        model = Message
        fields = ['id', 'content', 'direction', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """
    Serializador detalhado para o modelo Conversation, incluindo suas mensagens.
    """
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'state', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_messages(self, obj):
        """Retorna todas as mensagens da conversa, ordenadas por timestamp."""
        messages = obj.messages.all().order_by('timestamp')
        return MessageInConversationSerializer(messages, many=True).data


# conversation/services/conversation_service.py
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