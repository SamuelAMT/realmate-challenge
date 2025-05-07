from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import logging
from webhook.services.webhook_service import WebhookService

logger = logging.getLogger(__name__)


class WebhookView(APIView):
    """
    View para processar webhooks do sistema de atendimento.
    Recebe eventos de conversas e mensagens, e atualiza o banco de dados.
    """

    def post(self, request, *args, **kwargs):
        """
        Processa os eventos recebidos via webhook.

        Tipos de eventos:
        - NEW_CONVERSATION: Cria uma nova conversa
        - NEW_MESSAGE: Adiciona uma nova mensagem a uma conversa existente
        - CLOSE_CONVERSATION: Fecha uma conversa existente
        """
        try:
            # Extrair dados do webhook
            event_type = request.data.get('type')
            data = request.data.get('data', {})
            timestamp = request.data.get('timestamp')

            # Validação básica
            if not event_type or not data:
                return Response(
                    {"error": "Invalid webhook format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Processar evento usando o serviço
            service = WebhookService()
            result = service.process_event(event_type, data, timestamp)

            return Response(result["response"], status=result["status"])

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
