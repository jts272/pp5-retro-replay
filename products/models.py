from django.db import models
from django.db.models.query import QuerySet
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


# Create your models here.
class AvailableProductManager(models.Manager):
    """Manager to return only products that are set as visible.

    This makes the built-in `Product.objects` unavailable.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(visible=True)


class AllProductsManager(models.Manager):
    """Makes the built-in `<Model>.objects.all()` functionality available
    after creating custom managers.
    """

    def get_queryset(self):
        return super().get_queryset().all()


class Product(models.Model):
    CONDITION_CHOICES = [
        ("Sealed", "Sealed"),
        ("Like New", "Like New"),
        ("Very Good", "Very Good"),
        ("Good", "Good"),
        ("Acceptable", "Acceptable"),
    ]

    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["name"],
        help_text=(
            "This field is generated automatically when the product is saved. "
            "It cannot be edited."
        ),
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    platform = models.ForeignKey(
        "Platform", on_delete=models.SET_NULL, null=True, blank=True
    )
    region = models.ForeignKey(
        "Region", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(
        upload_to="product_images/%Y/%m/%d/", null=True, blank=True
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="Very Good"
    )
    description = models.TextField(default="Description coming soon!")
    sold = models.BooleanField(
        help_text=(
            "The product will automatically be marked as sold once"
            " payment has been completed"
        ),
        default=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(
        default=True,
        help_text=(
            "Select to make the product visible on the site. This can be"
            " unchecked to stop sold out products from appearing on the site."
        ),
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} for {self.platform} - {self.region}"

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def mark_as_sold(self):
        self.sold = True
        self.save()
        return self.sold

    # `objects` must be placed as top manager to show all products
    objects = AllProductsManager()
    available_products = AvailableProductManager()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    icon = models.ImageField(upload_to="regions/", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
