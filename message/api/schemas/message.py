from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Message.
    """
    class Meta:
        model = Message
        fields = ['message_id', 'content', 'direction', 'timestamp', 'conversation']
        read_only_fields = ['message_id', 'timestamp']
