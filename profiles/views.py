from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def profile(request):
    """Display the user's profile to perform actions relating to saved
    addresses and past orders.

    Arguments:
        request -- HttpRequest
    """
    context = {}
    return render(request, "profiles/profile.html", context)
