from django.db import models
import uuid
from django.core.exceptions import ValidationError
from conversation.models import Conversation


class Message(models.Model):
    """
    Representa uma mensagem em uma conversa.
    Uma mensagem possui uma direção (SENT ou RECEIVED) e está associada a uma conversa.
    """
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'

    DIRECTION_CHOICES = [
        (SENT, 'Sent'),
        (RECEIVED, 'Received'),
    ]

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField()
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} - {self.direction}"

    def clean(self):
        """
        Validação para garantir que mensagens não possam ser adicionadas a conversas fechadas
        """
        if not self.conversation.is_open:
            raise ValidationError(
                "Cannot add message to a closed conversation")

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a validação seja executada
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
