from django.test import TestCase
from conversation.models import Conversation
from message.models import Message
import uuid


class ConversationModelTestCase(TestCase):
    """Testes para o modelo Conversation"""

    def setUp(self):
        """Configuração para cada teste"""
        self.conversation_id = uuid.uuid4()
        self.conversation = Conversation.objects.create(
            id=self.conversation_id
        )

    def test_conversation_creation(self):
        """Testa a criação de uma conversa"""
        self.assertEqual(self.conversation.state, Conversation.OPEN)
        self.assertTrue(self.conversation.is_open)

    def test_conversation_close(self):
        """Testa o fechamento de uma conversa"""
        self.conversation.close()
        self.assertEqual(self.conversation.state, Conversation.CLOSED)
        self.assertFalse(self.conversation.is_open)

    def test_string_representation(self):
        """Testa a representação em string de uma conversa"""
        self.assertEqual(
            str(self.conversation),
            f"Conversation {self.conversation_id} - {Conversation.OPEN}"
        )
