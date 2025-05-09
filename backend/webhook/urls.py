from django.urls import path
from webhook.views import WebhookProcessorView

urlpatterns = [
    path('', WebhookProcessorView.as_view(), name='webhook-processor'),
]
