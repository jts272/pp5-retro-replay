from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.profile, name="profile"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<slug:order_id>/", views.order_detail, name="order_detail"),
    path("addresses/", views.address_list, name="address_list"),
    # Paths for CRUD functions
    path("addresses/add/", views.address_add, name="address_add"),
]
