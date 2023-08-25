from django.shortcuts import render

from products.models import Product


# Create your views here.
def home(request):
    """A view to render the home page and a selection of recent products.

    List slice notation is used to determine the number of recent products
    to return.

    Arguments:
        request -- HttpRequest

    Returns:
        HTML template with request and context variables available
    """
    recent_products = Product.objects.all().order_by("-created")[:4]
    context = {"recent_products": recent_products}
    return render(request, "home/home.html", context)
