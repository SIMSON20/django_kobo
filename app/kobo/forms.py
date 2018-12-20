from django import forms
from .models import Connection, KoboUser, KoboData
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q

class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        exclude = []
        widgets = {
            'auth_pass': forms.PasswordInput(),
            }


class KoboUserForm(forms.ModelForm):
    class Meta:
        model = KoboUser
        exclude = []

    surveys = forms.ModelMultipleChoiceField(queryset=KoboData.objects.filter(Q(tags__icontains=['bns']) | Q(tags__icontains=['nrgt'])), widget=FilteredSelectMultiple(
                                                'Surveys', is_stacked=False), label='')
