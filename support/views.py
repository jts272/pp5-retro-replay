from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django_summernote.widgets import SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField

from .models import FAQ


# Create your views here.
def support(request):
    faqs = FAQ.objects.filter(published=True)
    context = {"faqs": faqs}
    return render(request, "support/support.html", context)


class AddFAQ(CreateView):
    model = FAQ
    fields = ["question", "answer", "published"]
    answer = SummernoteTextField()
    widgets = {"answer": SummernoteInplaceWidget()}


class UpdateFAQ(UpdateView):
    model = FAQ
    fields = ["question", "answer", "published"]
    answer = SummernoteTextField()
    widgets = {"answer": SummernoteInplaceWidget()}


class DeleteFAQ(DeleteView):
    model = FAQ
    success_url = reverse_lazy("support:support")
