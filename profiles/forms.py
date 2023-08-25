import re

from django import forms
from django.utils.translation import gettext_lazy as _

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
        labels = {
            "address_line1": _("Address line 1"),
            "address_line2": _("Address line 2"),
        }

    # https://www.mattlayman.com/django-riffs/how-to-use-forms/
    def clean_name(self):
        # https://docs.python.org/3/howto/regex.html
        p = re.compile("[a-zA-z]+")
        name = self.cleaned_data["name"]
        if not p.match(name):
            raise forms.ValidationError(
                "Your name must contain at least one letter."
            )
        return name

    def clean_address_line1(self):
        p = re.compile("[a-zA-z0-9]+")
        address_line1 = self.cleaned_data["address_line1"]
        if not p.match(address_line1):
            raise forms.ValidationError(
                "Your first line address must contain at least one letter or"
                " number."
            )
        return address_line1

    def clean_address_line2(self):
        p = re.compile("[a-zA-z]+")
        address_line2 = self.cleaned_data["address_line2"]
        # This check is only performed if a value has been entered
        if address_line2:
            if not p.match(address_line2):
                raise forms.ValidationError(
                    "Your second line address must contain at least one letter"
                    " or number."
                )
            return address_line2

    def clean_city(self):
        p = re.compile("[a-zA-z]+")
        city = self.cleaned_data["city"]
        # This check is only performed if a value has been entered

        if not p.match(city):
            raise forms.ValidationError(
                "Your City must contain at least one letter."
            )
        return city

    def clean_postal_code(self):
        # Adapted from gov.uk 'Appendix C - Valid Postcode Format
        p = re.compile("[a-zA-Z][a-zA-z0-9][a-zA-z0-9\s]{1,6}")  # noqa
        postal_code = self.cleaned_data["postal_code"]
        if not p.match(postal_code):
            raise forms.ValidationError(
                "Please enter a valid British postcode."
            )
        return postal_code
