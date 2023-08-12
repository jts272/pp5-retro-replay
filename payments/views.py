import json
import os

import stripe
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from basket.basket import Basket

if os.path.isfile("env.py"):
    import env  # noqa


# Create your views here.
def checkout(request):
    # https://youtu.be/ncsCnC3Ynlw?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=12452
    basket = Basket(request)

    if basket:
        print(basket.basket.keys())
        order_item_ids = {i for i in basket.basket.keys()}
        print(order_item_ids)

        # Get subtotal as integer with no decimals for Stripe
        total = str(basket.get_subtotal())
        total = total.replace(".", "")
        total = int(total)
        print(total)

        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        intent = stripe.PaymentIntent.create(
            amount=total,
            currency="gbp",
            metadata={
                "user_id": request.user.pk,
                "order_item_ids": order_item_ids,
            },
        )

        print(intent.client_secret)

        context = {"basket": basket, "client_secret": intent.client_secret}
    else:
        context = {
            "basket": basket,
            # "client_secret": intent.client_secret
        }
        print(basket.basket)
    return render(request, "payments/payments.html", context)


@require_POST
@csrf_exempt
def webhook_view(request):
    # Reference: https://stripe.com/docs/webhooks#example-endpoint
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
        # print(f"webhook payment intent: {payment_intent}")
        create_order(payment_intent)
    elif event.type == "payment_method.attached":
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        print(f"webhook payment_method: {payment_method}")
    # ... handle other event types
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)


# Webhook handler functions
def create_order(stripe_response):
    # Get data returned from Stripe to create the Order instance
    # Key: model field, Value: Stripe JSON response
    print(f"full Stripe response: {stripe_response}")
    data = stripe_response
    returned_data = {
        "name": data.shipping.name,
        "address_line1": data.shipping.address.line1,
        "address_line2": data.shipping.address.line2,
        "city": data.shipping.address.city,
        "postal_code": data.shipping.address.postal_code,
        "amount": data.amount,
        "paid": True,
    }
    print(returned_data)
