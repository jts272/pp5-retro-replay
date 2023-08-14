import uuid

from django.db import models

from products.models import Product


# Create your models here.
class Order(models.Model):
    """A model to store an instance of an order.

    The instance is created when the payment form is submitted. On successful
    return from the webhook, the `paid` field is set to `True`.

    See the Stripe docs on the `PaymentIntent` object for more information
    on the fields returned from the webhook:

    https://stripe.com/docs/api/payment_intents/object
    """

    # A unique identifier to perform checks against
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # Shipping information
    name = models.CharField(max_length=80)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=10)
    # Transactional information
    # Payment intent returns an integer - format in webhook to create decimal
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name}'s order on {self.created}"


class OrderItem(models.Model):
    """A model to represent each individual item in a related order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # For instances where the item may be discounted
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price paid at time of purchase",
    )

    def __str__(self):
        return f"Order Item id: {self.pk} - Item: {self.product}"
