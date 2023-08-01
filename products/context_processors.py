from .models import Category, Platform


def categories(request):
    """Context processor to make Categories available in template context.

    Arguments:
        request -- HttpRequest
    """
    return {"categories": Category.objects.all()}


def platforms(request):
    """Context processor to make Platforms available in template context.

    Arguments:
        request -- HttpRequest
    """
    return {"platforms": Platform.objects.all()}
