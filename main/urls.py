from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conversations/', include('conversation.urls')),
    path('webhook/', include('webhook.urls')),
]
