from django.shortcuts import render
from .models import FAQ


# Create your views here.
def support(request):
    faqs = FAQ.objects.filter(published=True)
    context = {"faqs": faqs}
    return render(request, "support/support.html", context)
