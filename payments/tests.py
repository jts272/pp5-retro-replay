from django.contrib.auth.models import User
from django.test import Client, TestCase


# Create your tests here.
class TestBasketView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")

    def test_checkout_url_200(self):
        response = self.c.get("/payments/checkout/")
        self.assertEqual(response.status_code, 200)

    def test_checkout_status_url_200(self):
        response = self.c.get("/payments/checkout-status/")
        self.assertEqual(response.status_code, 200)
