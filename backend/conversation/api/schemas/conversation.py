from rest_framework import serializers
from conversation.models import Conversation
from message.models import Message


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializador básico para o modelo Conversation.
    """

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'state', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']


class MessageInConversationSerializer(serializers.ModelSerializer):
    """
    Serializador para mensagens dentro do contexto de uma conversa.
    """

    class Meta:
        model = Message
        fields = ['message_id', 'content', 'direction', 'timestamp']
        read_only_fields = ['message_id', 'timestamp']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """
    Serializador detalhado para o modelo Conversation, incluindo suas mensagens.
    """
    messages = MessageInConversationSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'state', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def get_messages(self, obj):
        """Retorna todas as mensagens da conversa, ordenadas por timestamp."""
        messages = obj.messages.all().order_by('timestamp')
        return MessageInConversationSerializer(messages, many=True).data