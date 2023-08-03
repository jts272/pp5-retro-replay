from .basket import Basket


def basket(request):
    """Context processor to make Basket data available in template context.

    Arguments:
        request -- HttpRequest

    Returns:
        Basket instance which is initialized from request session data
    """
    return {"basket": Basket(request)}
