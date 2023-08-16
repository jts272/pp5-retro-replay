from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from orders.models import Order

from .models import Address, Profile


# Create your views here.
@login_required
def profile(request):
    """The landing page for the logged in user's profile management
    tools. From here they can select appropriate address or order history
    actions.

    Arguments:
        request -- HttpRequest
    """
    profile = get_object_or_404(Profile, user=request.user)
    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)


@login_required
def order_list(request):
    """Displays a list of the user's past orders, which they may select
    to view in more detail.

    Arguments:
        request -- HttpRequest
    """
    profile = get_object_or_404(Profile, user=request.user)
    # Use the selected profile to get its related orders
    orders = profile.order_set.all()
    context = {"profile": profile, "orders": orders}
    return render(request, "profiles/order_list.html", context)


@login_required
def order_detail(request, order_id):
    # Match order by order id (uuid) and the profile of the current user
    order = get_object_or_404(
        Order, order_id=order_id, profile=request.user.profile
    )
    items = order.orderitem_set.all()
    context = {"order": order, "items": items}
    return render(request, "profiles/order_detail.html", context)


@login_required
def address_list(request):
    addresses = Address.objects.filter(profile=request.user.profile)
    context = {"addresses": addresses}
    return render(request, "profiles/address_list.html", context)
