import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    """Extends Django's built-in user model, for the purposes of creating,
    updating and deleting saved address records and viewing past orders.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Creates or updates a profile instance when a Django user is
    created or updated using signals.

    Arguments:
        sender -- model that sends the signal
        instance -- instance being saved
        created -- boolean which is True if the record was created

    Reference:
    https://youtu.be/YOf1GMOD9Bc?t=126
    https://docs.djangoproject.com/en/3.2/ref/signals/#post-save
    """
    if created:
        Profile.objects.create(user=instance)
    # Save the profile for existing users
    # instance.profile.save()


class Address(models.Model):
    """Allows a user to create, update and delete addresses to prefill
    the Stripe address form for a faster checkout.

    Reference:
    https://youtu.be/8SP76dopYVo?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=749
    """

    # The profile that this address instance is linked to
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # uuid used as a unique slug for the user's CRUD functions
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    # Fields to prefill Stripe address form; these mirror the order model
    name = models.CharField(max_length=80)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=10)
    # Bookkeeping fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # User must select a default address to prefill Stripe address form
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Saved Address"
