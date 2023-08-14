from django.urls import path

from . import views

app_name = "payments"
urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("webhook/", views.webhook_view, name="webhook"),
    path("checkout-status/", views.checkout_status, name="checkout_status"),
]
