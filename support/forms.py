from django import forms
from .models import FAQ
from django_summernote.widgets import SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField


class FAQform(forms.ModelForm):
    # https://github.com/summernote/django-summernote#form
    class Meta:
        model = FAQ
        fields = ["question", "answer", "published"]
        answer = SummernoteTextField()
        widgets = {"answer": SummernoteInplaceWidget()}
