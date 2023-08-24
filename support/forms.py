import re

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
        widgets = {
            "query": forms.widgets.Textarea(
                attrs={
                    "placeholder": (
                        "Enter you query here (minimum 20 characters)"
                    )
                }
            )
        }

    def clean_query(self):
        p = re.compile("[a-zA-z]{1-20}")
        query = self.cleaned_data["query"]
        if not p.match(query):
            raise forms.ValidationError(
                "Please provide some more detail before submitting your query."
            )
        return query
