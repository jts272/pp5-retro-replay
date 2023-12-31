import uuid

from django.db import models
from django.urls import reverse

from products.models import Product
from profiles.models import Profile


# Create your models here.
class Order(models.Model):
    """A model to store an instance of an order.

    The instance is created when the payment form is submitted. On successful
    return from the webhook, the `paid` field is set to `True`.

    See the Stripe docs on the `PaymentIntent` object for more information
    on the fields returned from the webhook:

    https://stripe.com/docs/api/payment_intents/object
    """

    # Delivery charge variables
    STANDARD_DELIVERY_CHARGE = 1.99
    FREE_DELIVERY_THRESHOLD = 30

    # A unique identifier to perform checks against
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # Link each order to a profile, which is linked to a Django user instance
    # Set null to keep the order if the user gets deleted
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    # Shipping information
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=10)
    # Transactional information
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_charge = models.DecimalField(
        max_digits=4, decimal_places=2, default=STANDARD_DELIVERY_CHARGE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Completed at")
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name}'s order on {self.created}"

    def get_absolute_url(self):
        return reverse(
            "profiles:order_detail", kwargs={"order_id": self.order_id}
        )


class OrderItem(models.Model):
    """A model to represent each individual item in a related order."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price paid at time of purchase",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Order Item id: {self.pk} - Item: {self.product}"
