from django.shortcuts import render

from basket.basket import Basket


# Create your views here.
def checkout(request):
    # https://youtu.be/ncsCnC3Ynlw?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=12452
    basket = Basket(request)

    # Get subtotal as integer with no decimals for Stripe
    total = str(basket.get_subtotal())
    total = total.replace(".", "")
    total = int(total)
    print(total)

    context = {"basket": basket}
    return render(request, "payments/payments.html", context)
