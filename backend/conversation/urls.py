from django.urls import path, include
from rest_framework.routers import DefaultRouter

from conversation.api.routes.conversation import ConversationViewSet
from message.api.routes.message import MessageListCreateAPIView

app_name = "conversation"

router = DefaultRouter()
router.register(r"", ConversationViewSet, basename="conversation")

urlpatterns = [
    path("", include(router.urls)),
    path("<uuid:conversation_id>/messages/", MessageListCreateAPIView.as_view(), name="message-list-create"),
]
