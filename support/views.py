from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def support(request):
    return HttpResponse("This is the support page")
