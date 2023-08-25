from .models import Category, Platform, Region


def categories(request):
    """Context processor to make Categories available in template context.

    This is used to populate navbar entries.

    Arguments:
        request -- HttpRequest

    Returns:
        Context dictionary for categories
    """
    return {"categories": Category.objects.all()}


def platforms(request):
    """Context processor to make Platforms available in template context.

    This is used to populate navbar entries.

    Arguments:
        request -- HttpRequest

    Returns:
        Context dictionary for platforms
    """
    return {"platforms": Platform.objects.all()}


def regions(request):
    """Context processor to make Regions available in template context.

    This is used to populate navbar entries.

    Arguments:
        request -- HttpRequest

    Returns:
        Context dictionary for regions
    """
    return {"regions": Region.objects.all()}
