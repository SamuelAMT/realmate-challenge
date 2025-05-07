from django.contrib import admin
from conversation.models import Conversation
from conversation.forms import ConversationForm


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Conversation.
    """
    form = ConversationForm
    list_display = ['conversation_id', 'state', 'created_at', 'updated_at']
    list_filter = ['state', 'created_at']
    search_fields = ['conversation_id']
    readonly_fields = ['conversation_id', 'created_at', 'updated_at']