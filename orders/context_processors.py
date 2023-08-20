from .models import Order


def delivery_charges(request):
    """Context processor to make delivery variables from the Order model
    available in templates

    Arguments:
        request -- HttpRequest

    Returns:
        Current standard delivery charge and free delivery threshold
    """
    context = {
        "standard_delivery_charge": Order.STANDARD_DELIVERY_CHARGE,
        "free_delivery_threshold": Order.FREE_DELIVERY_THRESHOLD,
    }
    return context
