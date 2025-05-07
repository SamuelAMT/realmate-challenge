from django.urls import path
from webhook.views import WebhookView

urlpatterns = [
    path('', WebhookView.as_view(), name='webhook'),
]
