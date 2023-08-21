from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from .models import FAQ, CustomerQuery


class FAQForm(forms.ModelForm):
    # https://github.com/summernote/django-summernote#form
    class Meta:
        model = FAQ
        fields = ["question", "answer", "published"]
        answer = SummernoteTextField()
        widgets = {"answer": SummernoteWidget()}


class CustomerQueryForm(forms.ModelForm):
    class Meta:
        model = CustomerQuery
        fields = ["query"]
        widgets = {"query": forms.widgets.Textarea()}
