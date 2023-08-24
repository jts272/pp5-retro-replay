import factory
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ProfileAddressForm
from .models import Profile, Address


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "Joe"


class ProfileFactory(factory.Factory):
    class Meta:
        model = Profile

    user = UserFactory()


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    name = "Joe"
    address_line1 = "123 Street"
    address_line2 = "Flat A"
    city = "London"
    postal_code = "SW1A 2AA"


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


class TestProfileModel(TestCase):
    def test_profile_str_method(self):
        self.p = ProfileFactory()
        self.assertEqual(self.p.__str__(), "Joe")

    def test_profile_get_address_object_method(self):
        self.a = AddressFactory()
        response = self.a.get_address_object()
        self.assertEqual(
            response,
            {
                "name": "Joe",
                "address": {
                    "line1": "123 Street",
                    "line2": "Flat A",
                    "city": "London",
                    "postal_code": "SW1A 2AA",
                    "country": "GB",
                },
            },
        )
