from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteInplaceWidget

from .models import FAQ


# Create your views here.
def support(request):
    faqs = FAQ.objects.filter(published=True)
    context = {"faqs": faqs}
    return render(request, "support/support.html", context)


class AddFAQ(SuccessMessageMixin, CreateView):
    model = FAQ
    fields = ["question", "answer", "published"]
    answer = SummernoteTextField()
    widgets = {"answer": SummernoteInplaceWidget()}
    success_url = reverse_lazy("support:support")
    success_message = "New FAQ has been added!"


class UpdateFAQ(SuccessMessageMixin, UpdateView):
    model = FAQ
    fields = ["question", "answer", "published"]
    answer = SummernoteTextField()
    widgets = {"answer": SummernoteInplaceWidget()}
    success_url = reverse_lazy("support:support")
    success_message = "Your FAQ has been updated."


class DeleteFAQ(DeleteView):
    model = FAQ
    success_url = reverse_lazy("support:support")
    success_message = "Your FAQ has been deleted."

    # Give message for deletion - cannot use mixin to hook to form_valid
    # Reference: https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteFAQ, self).delete(request, *args, **kwargs)
