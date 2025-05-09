from django import forms
from message.models import Message


class MessageForm(forms.ModelForm):
    """
    Formulário para o modelo Message no admin.
    """
    class Meta:
        model = Message
        fields = ['conversation', 'content', 'direction']
