from django.contrib import admin
from message.models import Message
from message.forms import MessageForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Message.
    """
    form = MessageForm
    list_display = ['message_id', 'conversation', 'direction', 'timestamp']
    list_filter = ['direction', 'timestamp', 'conversation__state']
    search_fields = ['message_id', 'content', 'conversation__conversation_id']
    readonly_fields = ['message_id', 'timestamp']
