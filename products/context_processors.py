from .models import Category


def categories(request):
    """Context processor to make Categories available in template context.

    Arguments:
        request -- HttpRequest
    """
    return {"categories": Category.objects.all()}
