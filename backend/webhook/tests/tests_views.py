from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from conversation.models import Conversation
from message.models import Message
import uuid
import json


class WebhookViewTestCase(TestCase):
    """Testes para a view de processamento de webhook"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = APIClient()
        self.webhook_url = reverse('webhook-processor')
        self.conversation_id = str(uuid.uuid4())
        self.message_id = str(uuid.uuid4())

    def test_new_conversation_webhook(self):
        """Testa o processamento de um webhook de nova conversa"""
        payload = {
            "type": "NEW_CONVERSATION",
            "timestamp": "2025-02-21T10:20:41.349308",
            "data": {
                "conversation_id": self.conversation_id
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conversation.objects.count(), 1)

        conversation = Conversation.objects.get(conversation_id=self.conversation_id)
        self.assertEqual(conversation.state, Conversation.OPEN)

    def test_new_message_webhook(self):
        """Testa o processamento de um webhook de nova mensagem"""
        # Primeiro cria a conversa
        Conversation.objects.create(conversation_id=self.conversation_id)

        # Payload para nova mensagem
        payload = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:42.349308",
            "data": {
                "message_id": self.message_id,
                "direction": "RECEIVED",
                "content": "Olá, tudo bem?",
                "conversation_id": self.conversation_id
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.get(message_id=self.message_id)
        self.assertEqual(message.content, "Olá, tudo bem?")
        self.assertEqual(message.direction, Message.RECEIVED)

    def test_close_conversation_webhook(self):
        """Testa o processamento de um webhook de fechamento de conversa"""
        # Primeiro cria a conversa
        Conversation.objects.create(conversation_id=self.conversation_id)

        # Payload para fechar conversa
        payload = {
            "type": "CLOSE_CONVERSATION",
            "timestamp": "2025-02-21T10:20:45.349308",
            "data": {
                "conversation_id": self.conversation_id
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        conversation = Conversation.objects.get(conversation_id=self.conversation_id)
        self.assertEqual(conversation.state, Conversation.CLOSED)

    def test_message_to_closed_conversation(self):
        """Testa que não é possível adicionar mensagens a conversas fechadas via webhook"""
        # Cria e fecha a conversa
        conversation = Conversation.objects.create(conversation_id=self.conversation_id)
        conversation.close()

        # Tenta adicionar mensagem
        payload = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:42.349308",
            "data": {
                "message_id": self.message_id,
                "direction": "RECEIVED",
                "content": "Esta mensagem não deve ser aceita",
                "conversation_id": self.conversation_id
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Nenhuma mensagem deve ser criada
        self.assertEqual(Message.objects.count(), 0)
