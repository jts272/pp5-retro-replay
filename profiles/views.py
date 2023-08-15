from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from profiles.models import Profile


# Create your views here.
@login_required
def profile(request):
    """Display the user's profile to perform actions relating to saved
    addresses and past orders.

    Arguments:
        request -- HttpRequest
    """
    profile = get_object_or_404(Profile, user=request.user)
    # Use the selected profile to get its related orders
    orders = profile.order_set.all()
    context = {"profile": profile, "orders": orders}
    return render(request, "profiles/profile.html", context)
