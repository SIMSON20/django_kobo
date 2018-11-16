from django import forms
from .models import Connection


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        widgets = {
        'auth_pass': forms.PasswordInput(),
    }