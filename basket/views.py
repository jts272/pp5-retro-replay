from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render

from products.models import Product

from .basket import Basket


# Create your views here.
def basket_summary(request):
    return render(request, "basket/basket.html")


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
        print(f"product pk = {product.pk}")

        if str(product.pk) not in basket.basket.keys():
            # Add product to the Basket instance
            basket.add(product=product)
        else:
            print("already added!")

        response = JsonResponse({"product": product.pk})
        print(f"response.content: {response.content}")
        print(f"basket: {basket.basket}")
        print(f"basket keys: {basket.basket.keys()}")
        print(f"basket length: {basket.__len__()}")
        return response
