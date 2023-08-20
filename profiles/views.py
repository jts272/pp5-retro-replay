from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from orders.models import Order

from .forms import ProfileAddressForm
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
    print(request.method)
    addresses = Address.objects.filter(profile=request.user.profile)
    context = {"addresses": addresses}
    return render(request, "profiles/address_list.html", context)


@login_required
def address_add(request):
    """Adds an address model instance to the user's profile.

    In addition to manually entered fields, the address instance is
    attached to the user's profile. The uuid field is automatically
    generated from the field's own `default` attribute when created.

    Arguments:
        request -- HttpRequest

    Returns:
        Template for user to enter valid saved address information.
        Redirects to address list page on success.

    Reference:
    https://youtu.be/8SP76dopYVo?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=2825
    """
    if request.method == "POST":
        form = ProfileAddressForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.profile = request.user.profile
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Your new address has been saved.",
            )
            return HttpResponseRedirect(reverse("profiles:address_list"))

    else:
        form = ProfileAddressForm()

    context = {"form": ProfileAddressForm()}
    return render(request, "profiles/address_form.html", context)


@login_required
def address_edit(request, uuid):
    if request.method == "POST":
        address = Address.objects.get(uuid=uuid, profile=request.user.profile)
        form = ProfileAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.INFO, "Your address has been updated."
            )
            return HttpResponseRedirect(reverse("profiles:address_list"))
    else:
        address = Address.objects.get(uuid=uuid, profile=request.user.profile)
        print(address)
        form = ProfileAddressForm(instance=address)
    context = {"form": form}
    return render(request, "profiles/address_form.html", context)


@login_required
def address_delete(request, uuid):
    """Delete the selected address instance.

    Arguments:
        request -- HttpRequest
        uuid -- Unique identifier for address object

    Returns:
        Removes the selected address and redirects to the list view

    Reference:
    https://youtu.be/8SP76dopYVo?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_
    """
    Address.objects.get(uuid=uuid, profile=request.user.profile).delete()
    messages.add_message(
        request, messages.ERROR, "Your address has been deleted."
    )
    return HttpResponseRedirect(reverse("profiles:address_list"))


@login_required
def address_set_default(request, uuid):
    """A view for setting a single default address from the list of
    saved addresses. Any existing address set as default will have its
    default property removed, so the newly selected address is the
    single selected default

    Arguments:
        request -- HttpRequest
        uuid -- Unique identifier for address object

    Returns:
        Selects the single address objects that has its `default` property
        set to `True`

    Reference:
    https://youtu.be/8SP76dopYVo?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=3873
    """
    # Get existing default address if present and set False
    Address.objects.filter(profile=request.user.profile, default=True).update(
        default=False
    )
    # Update the selected object's `default` property to True
    Address.objects.filter(uuid=uuid, profile=request.user.profile).update(
        default=True
    )
    messages.add_message(
        request, messages.SUCCESS, "Your default address has been set."
    )
    return HttpResponseRedirect(reverse("profiles:address_list"))
