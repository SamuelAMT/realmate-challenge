from django.urls import path
from webhook.api.routes.webhook import WebhookProcessorAPIView

app_name = "webhook"

urlpatterns = [
    path("", WebhookProcessorAPIView.as_view(), name="webhook-processor"),
]
