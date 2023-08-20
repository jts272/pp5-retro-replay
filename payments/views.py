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
from profiles.models import Address, Profile

if os.path.isfile("env.py"):
    import env  # noqa


# Create your views here.
@login_required
def checkout(request):
    """The main view for handling all payment information, which is
    passed to Stripe to generate the payment intent.

    Responsibilities:
        1. Get user's default saved address, if present
        2. Generate a JSON-style object to pass Stripe metadata
        3. Perform calculations to provide accurate grand total
        4. Create the `PaymentIntent` for Stripe payment

    Arguments:
        request -- HttpRequest

    Returns:
        Template with context for submitting payment to Stripe. If the
        basket is empty, only the basket context is returned and no Stripe
        elements are rendered.

    Reference:
    https://youtu.be/ncsCnC3Ynlw?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=12452
    """
    # 1. Get user's default saved address, if present
    # Null address object unless found in query
    address_object = None
    address_object_json = None
    if request.user.profile.address_set.exists():
        try:
            print("Addresses exist on this profile")
            # Select the user's default saved address from profile
            address = Address.objects.get(
                profile=request.user.profile, default=True
            )
            # Get the address object from the model method
            address_object = address.get_address_object()
            # Convert to JSON before handing off to template context
            address_object_json = json.dumps(address_object)
        except Exception as e:
            print(f"Exception: {e} No default address is set on this profile.")
    else:
        print("No addresses exist on this profile.")

    # 2. Generate a JSON-style object to pass Stripe metadata
    basket = Basket(request)

    if basket:
        # Build a JSON-like order item dictionary
        basket_keys = list(basket.basket.keys())
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

        # 3. Perform calculations to provide accurate grand total
        # Basket subtotal before any calculations
        subtotal = float(basket.get_subtotal())
        print(f"BASKET SUBTOTAL: {subtotal}")

        # Calculate delivery charge
        delivery_charge = Order.STANDARD_DELIVERY_CHARGE
        if subtotal > Order.FREE_DELIVERY_THRESHOLD:
            delivery_charge = 0
        print(f"DELIVERY CHARGE: {delivery_charge}")

        # Calculate grand total
        # Two decimal places specified for float arithmetic
        grand_total = round(subtotal + delivery_charge, 2)
        print(f"GRAND TOTAL: {grand_total}")

        # Convert grand total to integer in pence for Stripe
        amount = int(grand_total * 100)
        print(f"STRIPE AMOUNT: {amount}")

        # 4. Create the `PaymentIntent` for Stripe payment
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="gbp",
            metadata={
                "user_id": request.user.pk,
                "user_email": request.user.email,
                "order_items": order_items,
                "profile": request.user.profile.pk,
                "delivery_charge": delivery_charge,
            },
        )

        context = {
            "basket": basket,
            "client_secret": intent.client_secret,
            "address_object_json": address_object_json,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "grand_total": grand_total,
        }
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
        "profile": metadata.profile,
        "delivery_charge": metadata.delivery_charge,
    }
    print(returned_data)

    # Create model entries using the data returned from the webhook
    # Order model
    try:
        # Get profile instance the order will be added to
        profile = Profile.objects.get(pk=metadata.profile)

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
            profile=profile,
            delivery_charge=metadata.delivery_charge,
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
    basket = Basket(request)
    print("calling basket.clear_session()!")
    basket.clear_session()
    print(f"basket: {basket}")
    print(f"basket basket: {basket.basket}")
    return render(request, "payments/payment_status.html")
