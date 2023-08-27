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
        widgets = {
            "question": forms.TextInput(
                attrs={
                    "placeholder": "Question title (minimum 10 characters)."
                }
            ),
            "answer": SummernoteWidget(),
        }

    def clean_question(self):
        p = re.compile(".{10,}")
        question = self.cleaned_data["question"]
        if not p.match(question):
            raise forms.ValidationError(
                "Please provide a longer title (minimum 10 characters)."
            )
        return question

    def clean_answer(self):
        # Pattern includes opening and closing `p` tags from Summernote
        p = re.compile(".{27,}")
        answer = self.cleaned_data["answer"]
        if not p.match(answer):
            raise forms.ValidationError(
                "Please write 20 or more characters in your answer."
            )
        return answer


class CustomerQueryForm(forms.ModelForm):
    class Meta:
        model = CustomerQuery
        fields = ["query"]
        widgets = {
            "query": forms.widgets.Textarea(
                attrs={
                    "placeholder": (
                        "Enter you query here (minimum 20 characters)."
                    )
                }
            )
        }

    def clean_query(self):
        p = re.compile(".{20,}")
        query = self.cleaned_data["query"]
        if not p.match(query):
            raise forms.ValidationError(
                "Please provide some more detail before submitting your query"
                " (at least 20 characters)."
            )
        return query
