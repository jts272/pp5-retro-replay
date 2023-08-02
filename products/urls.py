from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("all-products/", views.all_products, name="all_products"),
    path(
        "categories/<slug:category>/",
        views.products_by_category,
        name="products_by_category",
    ),
    path(
        "platforms/<slug:platform>/",
        views.products_by_platform,
        name="products_by_platform",
    ),
    path(
        "regions/<slug:region>/",
        views.products_by_region,
        name="products_by_region",
    ),
    path("view/<slug:slug>/", views.product_detail, name="product_detail"),
]
