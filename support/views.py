from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CustomerQueryForm, FAQForm
from .models import FAQ


# Create your views here.
def support(request):
    if request.method == "POST":
        form = CustomerQueryForm(request.POST)

        # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
        if form.is_valid():
            new_query = form.save(commit=False)
            new_query.sender = request.user.email
            new_query.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Thanks for sending your query. We will respond soon!",
            )
            return redirect(reverse("support:support"))
    else:
        form = CustomerQueryForm()

    faqs = FAQ.objects.filter(published=True)
    context = {"faqs": faqs, "form": form}
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
