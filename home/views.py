from django.shortcuts import render

from products.models import Product


# Create your views here.
def home(request):
    recent_products = Product.objects.all()[:3]
    context = {"recent_products": recent_products}
    return render(request, "home/home.html", context)
