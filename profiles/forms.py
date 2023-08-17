from django import forms

from .models import Address


class ProfileAddressForm(forms.ModelForm):
    """A form to capture address information. This form creates an
    address model instance, using the same form fields that a customer
    would enter manually on the Stripe address element.

    Reference:
    https://youtu.be/8SP76dopYVo?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=2825
    """

    class Meta:
        model = Address
        fields = [
            "name",
            "address_line1",
            "address_line2",
            "city",
            "postal_code",
        ]
