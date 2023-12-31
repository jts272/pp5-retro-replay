from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


# Create your models here.
class AvailableProductManager(models.Manager):
    """Manager to return only products that are set as visible.

    To use the built-in `objects` manager after creating a custom
    manager, is must be subclassed again explicitly in the model.
    """

    def get_queryset(self):
        return super().get_queryset().filter(visible=True, sold=False)


class SoldProductManager(models.Manager):
    """Manager to return products that have been sold."""

    def get_queryset(self):
        return super().get_queryset().filter(visible=True, sold=True)


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
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Please enter the price in decimal format, e.g. 9.99",
    )
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

    # Django default manager
    objects = models.Manager()
    available_products = AvailableProductManager()
    sold_products = SoldProductManager()


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
