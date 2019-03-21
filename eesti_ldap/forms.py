from django import forms

from django.utils.translation import ugettext_lazy as _


class IdCheckQueryCreateForm(forms.Form):
    input = forms.DateField(label=_('My birthday'))
