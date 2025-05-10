from rest_framework import generics, status
from rest_framework.response import Response
from webhook.api.schemas.webhook import WebhookSerializer
from webhook.services.webhook_service import WebhookService
from django.core.exceptions import ValidationError
import logging


class WebhookProcessorAPIView(generics.GenericAPIView):
    """
    API View for processing incoming webhooks.
    POST /api/webhook/
    """
    serializer_class = WebhookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = WebhookService.process_webhook(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing webhook: {str(e)}")

            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )