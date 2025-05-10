from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Realmate Challenge API",
        default_version='v1',
        description="API for managing conversations and messages via webhook",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tecnologia@realmate.com.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLs - everything under /api/ prefix
    path('api/conversations/', include('conversation.urls')),
    path('api/webhook/', include('webhook.urls')),

    # Swagger documentation URLs
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
