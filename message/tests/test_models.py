from django.test import TestCase
from django.core.exceptions import ValidationError
from conversation.models import Conversation
from message.models import Message
import uuid


class MessageModelTestCase(TestCase):
    """Testes para o modelo Message"""

    def setUp(self):
        """Configuração para cada teste"""
        self.conversation_id = uuid.uuid4()
        self.conversation = Conversation.objects.create(
            id=self.conversation_id
        )

        self.message_id = uuid.uuid4()
        self.message = Message.objects.create(
            id=self.message_id,
            conversation=self.conversation,
            content="Test message content",
            direction=Message.RECEIVED
        )

    def test_message_creation(self):
        """Testa a criação de uma mensagem"""
        self.assertEqual(self.message.content, "Test message content")
        self.assertEqual(self.message.direction, Message.RECEIVED)
        self.assertEqual(self.message.conversation, self.conversation)

    def test_message_to_closed_conversation(self):
        """Testa que não é possível adicionar mensagens a conversas fechadas"""
        self.conversation.close()

        # Tenta criar uma nova mensagem na conversa fechada
        with self.assertRaises(ValidationError):
            Message.objects.create(
                id=uuid.uuid4(),
                conversation=self.conversation,
                content="This should fail",
                direction=Message.SENT
            )

    def test_message_string_representation(self):
        """Testa a representação em string de uma mensagem"""
        self.assertIn(str(self.message_id), str(self.message))
        self.assertIn(Message.RECEIVED, str(self.message))
