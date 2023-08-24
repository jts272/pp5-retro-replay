import factory
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .forms import ProfileAddressForm
from .models import Address, Profile


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


class TestAddressModel(TestCase):
    def test_address_str_method(self):
        self.p = AddressFactory()
        self.assertEqual(self.p.__str__(), "Saved Address")


class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")

    def test_profile_view_url_200(self):
        response = self.c.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_order_list_view_url_200(self):
        response = self.c.get("/profile/orders/")
        self.assertEqual(response.status_code, 200)

    def test_address_list_view_url_200(self):
        response = self.c.get("/profile/addresses/")
        self.assertEqual(response.status_code, 200)
