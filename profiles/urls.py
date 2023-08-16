from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.profile, name="profile"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<slug:order_id>/", views.order_detail, name="order_detail"),
    path("addresses/", views.address_list, name="address_list"),
    # path(
    #     "addresses/<slug:uuid>/", views.address_detail, name="address_detail"
    # ),
    # Include urls for editing views as they are made
]
