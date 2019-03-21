from django import forms

from eesti_ldap.models import IdCheckQuery
from django.utils.translation import ugettext_lazy as _


class IdCheckQueryCreateForm(forms.ModelForm):
    class Meta:
        model = IdCheckQuery
        fields = ['input']
        labels = {
            'input': _('My birthday')
        }
