from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from basket.basket import Basket

from .models import Category, Platform, Product, Region


# Create your views here.
def all_products(request):
    """Returns all products from the database.

    The default queryset is delivered by the `available_products` manager.
    Users have the option to find sold items using the searchbar.

    Arguments:
        request -- HttpRequest

    Returns:
        HTML template with request and context variables available
    """
    products = Product.available_products.all()

    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(region__name__icontains=query)
            )
            products = products.filter(queries)

    all_products_view = True

    context = {"products": products, "all_products_view": all_products_view}

    return render(request, "products/product_list.html", context)


def products_by_category(request, category):
    """Returns all products within a given category.

    The default queryset is delivered by the `available_products` manager.
    Users have the option to find sold items using the searchbar.

    Arguments:
        request -- HttpRequest
        category -- category to filter products by

    Returns:
        HTML template with request and context variables available
    """
    products = Product.available_products.filter(category__slug=category)
    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(region__name__icontains=query)
            )
            products = products.filter(queries)

    # Navigation context
    collection = "category"
    filter = Category.objects.get(slug=category)

    context = {
        "products": products,
        "collection": collection,
        "filter": filter,
    }

    return render(request, "products/product_list.html", context)


def products_by_platform(request, platform):
    """Returns all products within a given platform.

    The default queryset is delivered by the `available_products` manager.
    Users have the option to find sold items using the searchbar.

    Arguments:
        request -- HttpRequest
        platform -- platform to filter products by

    Returns:
        HTML template with request and context variables available
    """
    products = Product.available_products.filter(platform__slug=platform)
    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(region__name__icontains=query)
            )
            products = products.filter(queries)

    # Navigation context
    collection = "platform"
    filter = Platform.objects.get(slug=platform)

    context = {
        "products": products,
        "collection": collection,
        "filter": filter,
    }

    return render(request, "products/product_list.html", context)


def products_by_region(request, region):
    """Returns all products within a given region.

    The default queryset is delivered by the `available_products` manager.
    Users have the option to find sold items using the searchbar.

    Arguments:
        request -- HttpRequest
        region -- region to filter products by

    Returns:
        HTML template with request and context variables available
    """

    products = Product.available_products.filter(region__slug=region)
    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            queries = (
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(region__name__icontains=query)
            )
            products = products.filter(queries)

    # Navigation context
    collection = "region"
    filter = Region.objects.get(slug=region)

    context = {
        "products": products,
        "collection": collection,
        "filter": filter,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    """Returns the detail page for a given product. Perform a check to
    see if the product is currently in the basket for conditional
    rendering of the add to basket button. This is handled by JavaScript
    AJAX in the first instance, however this check handles subsequent
    visits to the page where the item is in the basket.

    Arguments:
        request -- HttpRequest
        slug -- unique slug of the item to be returned

    Returns:
        HTML template with request and context variables available
    """
    product = get_object_or_404(Product, slug=slug)

    # Update basket controls if item is already in basket
    basket_keys = list(Basket(request).basket.keys())
    basket_list = [int(i) for i in basket_keys]

    context = {"product": product, "basket_list": basket_list}

    return render(request, "products/product_detail.html", context)
