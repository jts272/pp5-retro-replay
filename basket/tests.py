from django.test import TestCase

from products.models import Product


# Create your tests here.
class TestBasketView(TestCase):
    def test_view_url_200_response(self):
        response = self.client.get("/basket/")
        self.assertEqual(response.status_code, 200)


class TestAddToBasketView(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="test product", price=10.00)

    def test_view_url_json_response(self):
        """Test for the json response from the ajax function to add to basket.

        Reference: https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=15091
        """
        response = self.client.post(
            "/basket/add/",
            {"productId": 1, "action": "post"},
        )
        self.assertTrue(response.json(), {"product just added": 1})


class TestRemoveFromBasketView(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="test product", price=10.00)
        self.client.post(
            "/basket/add/",
            {"productId": 1, "action": "post"},
        )

    def test_view_url_json_response(self):
        response = self.client.post(
            "/basket/remove/",
            {"productId": 1, "action": "post"},
        )
        self.assertTrue(response.json(), {"basket quantity": 0})
