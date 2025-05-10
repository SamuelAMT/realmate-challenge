from rest_framework import generics
from rest_framework.response import Response
from webhook.api.schemas.webhook import WebhookSerializer


class WebhookProcessorAPIView(generics.GenericAPIView):
    """
    API View for processing incoming webhooks.
    POST /api/webhook/
    """
    serializer_class = WebhookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Process webhook data
        # ...

        return Response({"status": "received"})
