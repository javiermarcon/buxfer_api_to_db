from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from .models import *


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ()

AccountFormSet = modelformset_factory(Account, form=AccountForm, extra=0, can_delete=False)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ()

TagFormSet = modelformset_factory(Tag, form=AccountForm, extra=0, can_delete=False)
