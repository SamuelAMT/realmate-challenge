from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from conversation.models import Conversation
from message.models import Message
import uuid


class ConversationAPITestCase(TestCase):
    """Testes para a API de conversas"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = APIClient()
        self.conversation_id = uuid.uuid4()
        self.conversation = Conversation.objects.create(
            id=self.conversation_id
        )

        # Cria algumas mensagens para a conversa
        self.message1 = Message.objects.create(
            id=uuid.uuid4(),
            conversation=self.conversation,
            content="Mensagem 1",
            direction=Message.RECEIVED
        )

        self.message2 = Message.objects.create(
            id=uuid.uuid4(),
            conversation=self.conversation,
            content="Mensagem 2",
            direction=Message.SENT
        )

        self.detail_url = reverse('conversation-detail',
                                  args=[str(self.conversation_id)])

    def test_get_conversation_detail(self):
        """Testa a recuperação dos detalhes de uma conversa"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica os campos da conversa
        self.assertEqual(response.data['id'], str(self.conversation_id))
        self.assertEqual(response.data['state'], Conversation.OPEN)

        # Verifica as mensagens
        self.assertEqual(len(response.data['messages']), 2)

        # Verifica se as mensagens estão na ordem correta
        self.assertEqual(response.data['messages'][0]['content'], "Mensagem 1")
        self.assertEqual(response.data['messages'][0]['direction'],
                         Message.RECEIVED)

        self.assertEqual(response.data['messages'][1]['content'], "Mensagem 2")
        self.assertEqual(response.data['messages'][1]['direction'],
                         Message.SENT)

    def test_get_nonexistent_conversation(self):
        """Testa a resposta para uma conversa que não existe"""
        nonexistent_url = reverse('conversation-detail',
                                  args=[str(uuid.uuid4())])
        response = self.client.get(nonexistent_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
