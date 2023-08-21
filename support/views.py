from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import FAQForm
from .models import FAQ


# Create your views here.
def support(request):
    faqs = FAQ.objects.filter(published=True)
    context = {"faqs": faqs}
    return render(request, "support/support.html", context)


class AddFAQ(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = FAQ
    form_class = FAQForm
    success_url = reverse_lazy("support:support")
    success_message = "New FAQ has been added!"

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class UpdateFAQ(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = FAQ
    form_class = FAQForm
    success_url = reverse_lazy("support:support")
    success_message = "Your FAQ has been updated."

    def test_func(self):
        user = self.request.user
        return user.is_superuser


class DeleteFAQ(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FAQ
    success_url = reverse_lazy("support:support")
    success_message = "Your FAQ has been deleted."

    def test_func(self):
        user = self.request.user
        return user.is_superuser

    # Give message for deletion - cannot use mixin to hook to form_valid
    # Reference: https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteFAQ, self).delete(request, *args, **kwargs)
