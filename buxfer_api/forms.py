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
        fields = ['categoria', 'tipo_tag', 'discrecionalidad']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['discrecionalidad']

class EditDataForm(forms.Form):
    ''' Page and ids t show in the editing form of changed data '''
    next_page = forms.IntegerField()
    ids = forms.CharField(widget=forms.HiddenInput())
    current_page = forms.IntegerField(widget=forms.HiddenInput())
