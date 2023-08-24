from django.test import TestCase

from .forms import ProfileAddressForm


# Create your tests here.
class TestProfileAddressForm(TestCase):
    # https://www.obeythetestinggoat.com/book/chapter_simple_form.html
    def test_not_form_is_valid(self):
        form = ProfileAddressForm(
            data={
                "name": "@",
                "address_line1": "@",
                "address_line2": "@",
                "city": "@",
                "postal_code": "@",
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_is_valid(self):
        form = ProfileAddressForm(
            data={
                "name": "Joe",
                "address_line1": "123 Street",
                "address_line2": "Flat A",
                "city": "London",
                "postal_code": "SW1A 2AA",
            }
        )
        self.assertTrue(form.is_valid())
