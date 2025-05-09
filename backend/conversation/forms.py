from django import forms
from conversation.models import Conversation


class ConversationForm(forms.ModelForm):
    """
    Formulário para o modelo Conversation no admin.
    """

    class Meta:
        model = Conversation
        fields = ['state']
