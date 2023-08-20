from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from orders.models import Order
from products.models import Product

from .basket import Basket


# Create your views here.
@login_required
def basket_summary(request):
    """A summary of all the items in the user's basket.

    Arguments:
        request -- HttpRequest

    Returns:
        HTML template with request and context variables available
    """
    basket = Basket(request)
    context = {"basket": basket}
    return render(request, "basket/basket.html", context)


@login_required
def add_to_basket(request):
    """Adds the selected item to the basket from the session.

    Arguments:
        request -- HttpRequest

    Reference:
    https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=7447
    """
    # Session data to perform actions within the Basket class
    basket = Basket(request)
    # Test action specified in ajax script data dictionary
    if request.POST.get("action") == "post":
        # Get product id captured in ajax data dictionary
        product_id = str(request.POST.get("productId"))
        # Get the referenced product from the database
        product = get_object_or_404(Product, pk=product_id)

        if str(product.pk) not in basket.basket.keys():
            # Add product to the Basket instance
            basket.add(product=product)

        basket_qty = basket.__len__()
        basket_contents = basket.basket

        response = JsonResponse(
            {
                "product just added:": product.pk,
                "basket quantity": basket_qty,
                "basket contents": basket_contents,
            }
        )
        # view_basket_url = "/basket/"
        # messages.add_message(
        #     request,
        #     messages.SUCCESS,
        #     f"Item added to basket. <a href='{view_basket_url}'>View Basket</a>",
        # )
        # messages.add_message(request, messages.ERROR, "message")

        return response


@login_required
def remove_from_basket(request):
    """Removes a given product stored in the basket.

    Arguments:
        request -- HttpRequest

    Reference:
    https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=11585
    """
    # Session data to perform actions within the Basket class
    basket = Basket(request)
    # Test action specified in ajax script data dictionary
    if request.POST.get("action") == "post":
        # Get product id captured in ajax data dictionary
        product_id = str(request.POST.get("productId"))
        # Call basket method to remove product from the basket
        basket.remove(product=product_id)

        response = JsonResponse(
            {
                "product removed": product_id,
                "basket quantity": basket.__len__(),
                "basket subtotal": basket.get_subtotal(),
            }
        )

        return response


def print_basket(request):
    # Get the delivery charge, based on the basket subtotal
    basket = Basket(request)

    print(f"basket subtotal: {basket.get_subtotal()}")

    delivery_charge = Order.STANDARD_DELIVERY_CHARGE

    if basket.get_subtotal() > Order.FREE_DELIVERY_THRESHOLD:
        delivery_charge = 0

    print(f"delivery_charge: {delivery_charge}")
    return JsonResponse(
        {
            "basket subtotal": basket.get_subtotal(),
            "delivery charge": delivery_charge,
        }
    )
