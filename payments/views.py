import json
import os

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
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
    if request.user.profile.address_set.exists():
        try:
            # Select the user's default saved address from profile
            address = Address.objects.get(
                profile=request.user.profile, default=True
            )
            # Get the address object from the model method
            address_object = address.get_address_object()
            # Convert to JSON before handing off to template context
            address_object_json = json.dumps(address_object)
        except Address.DoesNotExist:
            address = None
    else:
        address_object_json = None

    # 2. Generate a JSON-style object to pass Stripe metadata
    basket = Basket(request)

    # Guard clause for accessing checkout page with an empty basket
    if not basket:
        context = {"basket": basket}

    else:
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

        # Calculate delivery charge
        delivery_charge = Order.STANDARD_DELIVERY_CHARGE
        if subtotal >= Order.FREE_DELIVERY_THRESHOLD:
            delivery_charge = 0

        # Calculate grand total
        # Two decimal places specified for float arithmetic
        grand_total = round(subtotal + delivery_charge, 2)

        # Convert grand total to integer in pence for Stripe
        amount = int(grand_total * 100)

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
            # Passed to form data attribute to autofill Stripe address element
            "address_object_json": address_object_json,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "grand_total": grand_total,
        }

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
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        # Contains a stripe.PaymentIntent
        payment_intent = event.data.object
        # Payment success handler function
        create_order(payment_intent)

    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Payment could not be taken. Contact us for further information.",
        )
        return redirect(reverse("home:home"))

    return HttpResponse(status=200)


# Webhook handler functions
def create_order(stripe_response):
    data = stripe_response
    address = stripe_response.shipping
    metadata = stripe_response.metadata

    # Create order model instance
    try:
        # Get profile instance the order will be added to
        profile = Profile.objects.get(pk=metadata.profile)
    except Profile.DoesNotExist:
        profile = None

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

    # Create order items model instance(s)
    # Parse JSON string to Python object
    py_metadata = json.loads(metadata.order_items)
    # Get list of primary keys for each item ordered
    ordered_items = [i for i in py_metadata.values()]
    # Create an order item entry for each item in the list

    for i in range(len(ordered_items)):
        # Get the database entry of the product ordered
        try:
            product = Product.objects.get(pk=ordered_items[i]["id"])
        except Product.DoesNotExist:
            product = None

        # Create an order item instance for each ordered item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            # Price returned in decimal format from webhook metadata
            price=ordered_items[i]["price"],
        )

        # Mark each order item paid for as sold
        product.mark_as_sold()
        # Save each item created
        order_item.save()

    # Send email to customer with order context information
    # Requires email host and password environment variables to be set
    send_confirmation_email(order)


def checkout_status(request):
    # User is redirected here by Stripe.js after payment
    basket = Basket(request)
    basket.clear_session()
    return render(request, "payments/payment_status.html")


def send_confirmation_email(order):
    sender = settings.DEFAULT_FROM_EMAIL
    recipient = order.email
    title = render_to_string(
        "includes/email/order-confirm-title.txt", {"order": order}
    )
    body = render_to_string(
        "includes/email/order-confirm-body.txt", {"order": order}
    )
    send_mail(title, body, sender, [recipient])
