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
        return f"Conversation {self.conversation_id} - {self.state}"

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
