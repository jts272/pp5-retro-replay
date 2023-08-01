from django.shortcuts import render, get_object_or_404

from .models import Product


# Create your views here.
def all_products(request):
    """Returns all products from the database.

    Arguments:
        request -- HttpRequest

    Returns:
        HTML template with request and context variables available
    """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "products/index.html", context)


def products_by_category(request, category):
    """Returns all products within a given category.

    Arguments:
        request -- HttpRequest
        category -- category to filter products by

    Returns:
        HTML template with request and context variables available
    """
    products = Product.objects.filter(category__slug=category)
    context = {"products": products}
    return render(request, "products/index.html", context)


def products_by_platform(request, platform):
    """Returns all products within a given platform.

    Arguments:
        request -- HttpRequest
        platform -- platform to filter products by

    Returns:
        HTML template with request and context variables available
    """
    products = Product.objects.filter(platform__slug=platform)
    context = {"products": products}
    return render(request, "products/index.html", context)


def products_by_region(request, region):
    """Returns all products within a given region.

    Arguments:
        request -- HttpRequest
        region -- region to filter products by

    Returns:
        HTML template with request and context variables available
    """
    products = Product.objects.filter(region__slug=region)
    context = {"products": products}
    return render(request, "products/index.html", context)


def product_detail(request, pk):
    """Returns the detail page for a given product.

    Arguments:
        request -- HttpRequest
        pk -- Primary Key of the item to be returned

    Returns:
        HTML template with request and context variables available
    """
    product = get_object_or_404(Product, id=pk)
    context = {"product": product}
    return render(request, "products/product_detail.html", context)
