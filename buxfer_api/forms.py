from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from .models import *


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['tipo_pago']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['categoria', 'tipo_tag']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['discrecionalidad']
