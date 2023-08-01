from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.all_products, name="all_products"),
    path(
        "categories/<slug:category>/",
        views.products_by_category,
        name="products_by_category",
    ),
]
