import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from basket.basket import Basket
from orders.models import Order, OrderItem
from products.models import Product
from profiles.models import Address

if os.path.isfile("env.py"):
    import env  # noqa


# Create your views here.
@login_required
def checkout(request):
    if request.user.profile.address_set.exists():
        print("addresses exist on this profile")
        # Which address are we interested in
        address = Address.objects.get(
            profile=request.user.profile, default=True
        )
        print(address.get_address_object())

    else:
        print("No addresses exist on this profile")

    # https://youtu.be/ncsCnC3Ynlw?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=12452
    basket = Basket(request)

    print(request.user.email)

    if basket:
        # Build a JSON-like order item dictionary
        basket_keys = list(basket.basket.keys())
        print(basket.basket)
        order_items = {}
        for i in range(len(basket)):
            order_items.update(
                {
                    f"order_item{i + 1}": {
                        "id": f"{basket_keys[i]}",
                        "price": f"{basket.basket[basket_keys[i]]['price']}",
                    }
                }
            )

        # Format as JSON to pass to Stripe as metadata
        order_items = json.dumps(order_items)
        print(order_items)

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
                "user_email": request.user.email,
                "order_items": order_items,
            },
        )

        context = {"basket": basket, "client_secret": intent.client_secret}
    else:
        # Client secret not present as no Stripe elements will be built
        context = {"basket": basket}

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
    address = stripe_response.shipping
    metadata = stripe_response.metadata
    returned_data = {
        "name": address.name,
        "email": metadata.user_email,
        "address_line1": address.address.line1,
        "address_line2": address.address.line2,
        "city": address.address.city,
        "postal_code": address.address.postal_code,
        "amount": data.amount,
        "paid": True,
        "order_items": metadata.order_items,
    }
    print(returned_data)

    # Create model entries using the data returned from the webhook
    # Order model
    try:
        order = Order.objects.create(
            name=address.name,
            email=metadata.user_email,
            address_line1=address.address.line1,
            address_line2=address.address.line2,
            city=address.address.city,
            postal_code=address.address.postal_code,
            # Create decimal value from integer returned by Stripe
            amount=data.amount / 100,
            paid=True,
        )
        order.save()
    except Exception as e:
        print(f"ERROR: {e}")

    # Order items model
    try:
        # Parse JSON string to Python object
        py_metadata = json.loads(metadata.order_items)
        # Get list of primary keys for each item ordered
        ordered_items = [i for i in py_metadata.values()]
        # Create an order item entry for each item in the list
        for i in range(len(ordered_items)):
            order_item = OrderItem.objects.create(
                # Attach to newly created order
                order=order,
                # Get product by PK sent with Stripe metadata
                product=Product.objects.get(pk=ordered_items[i]["id"]),
                # Price returned in decimal format from webhook metadata
                price=ordered_items[i]["price"],
            )

        order_item.save()

    except Exception as e:
        print(f"ERROR: {e}")


def checkout_status(request):
    # User is redirected here by Stripe.js after payment
    return render(request, "payments/payment_status.html")
