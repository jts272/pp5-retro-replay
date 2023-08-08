import os

import stripe
from django.shortcuts import render

from basket.basket import Basket

if os.path.isfile("env.py"):
    import env  # noqa


# Create your views here.
def checkout(request):
    # https://youtu.be/ncsCnC3Ynlw?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=12452
    basket = Basket(request)

    # Get subtotal as integer with no decimals for Stripe
    total = str(basket.get_subtotal())
    total = total.replace(".", "")
    total = int(total)
    print(total)

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    intent = stripe.PaymentIntent.create(
        amount=total, currency="gbp", metadata={"user_id": request.user.pk}
    )

    print(intent.client_secret)

    context = {"basket": basket, "client_secret": intent.client_secret}
    return render(request, "payments/payments.html", context)
