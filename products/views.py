from django.shortcuts import render

from .models import Product


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "products/index.html", context)


def products_by_category(request, category):
    """Returns all products within a given category

    Arguments:
        request -- HttpRequest
        category -- category to filter products by
    """
    products = Product.objects.filter(category__slug=category)
    context = {"products": products}
    return render(request, "products/index.html", context)


def products_by_platform(request, platform):
    """Returns all products within a given platform

    Arguments:
        request -- HttpRequest
        platform -- platform to filter products by
    """
    products = Product.objects.filter(platform__slug=platform)
    context = {"products": products}
    return render(request, "products/index.html", context)
