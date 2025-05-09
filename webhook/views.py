from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import json
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from webhook.services.webhook_service import WebhookService

logger = logging.getLogger(__name__)


class WebhookProcessorView(APIView):
    """
    View para processar webhooks recebidos.
    Manipula eventos relacionados a conversas e mensagens.
    """

    @swagger_auto_schema(
        operation_summary="Processa webhooks",
        operation_description="Processa eventos de conversas e mensagens enviados via webhook",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['type', 'data'],
            properties={
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Tipo do evento: NEW_CONVERSATION, NEW_MESSAGE ou CLOSE_CONVERSATION"
                ),
                'timestamp': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Timestamp do evento"
                ),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Dados específicos do evento"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Webhook processado com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Erro no processamento do webhook",
            500: "Erro interno no servidor"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Processa webhooks POST recebidos.

        Formatos suportados:
        - NEW_CONVERSATION: Cria uma nova conversa
        - NEW_MESSAGE: Adiciona uma nova mensagem a uma conversa existente
        - CLOSE_CONVERSATION: Fecha uma conversa existente
        """
        try:
            # Processamento do webhook via serviço
            result = WebhookService.process_webhook(request.data)

            if result.get('success'):
                return Response(
                    {"status": "success", "message": result.get('message')},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "error", "message": result.get('message')},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except json.JSONDecodeError:
            logger.warning("Invalid JSON format in webhook")
            return Response(
                {"status": "error", "message": "Invalid JSON format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(f"Unexpected error processing webhook: {str(e)}")
            return Response(
                {"status": "error", "message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
