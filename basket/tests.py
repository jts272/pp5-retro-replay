from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from basket.basket import Basket
from products.models import Product


# Create your tests here.
class TestBasketView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()

    def test_authenticated_url_200(self):
        self.c.login(username="tester", password="secret")
        response = self.c.get("/basket/")
        self.assertEqual(response.status_code, 200)

    def test_authenticated_template_used(self):
        self.c.login(username="tester", password="secret")
        response = self.c.get("/basket/")
        self.assertTemplateUsed(response, "basket/basket.html")

    def test_unauthenticated_url_redirect(self):
        response = self.c.get("/basket/")
        self.assertRedirects(response, "/accounts/login/?next=/basket/")


class TestAddToBasketView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")
        self.p = Product.objects.create(name="test product", price=10.00)
        self.p.save()

    def test_view_url_json_response(self):
        """Test for the json response from the ajax function to add to basket.

        Reference:
        https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=15091
        """
        response = self.c.post(
            "/basket/add/", {"productId": 1, "action": "post"}
        )
        self.assertEqual(
            response.json(),
            {
                "product just added:": 1,
                "basket quantity": 1,
                "basket contents": {"1": {"price": "10.00"}},
            },
        )

    def test_http_get_redirects(self):
        response = self.c.get("/basket/add/")
        self.assertRedirects(response, reverse("products:all_products"))


class TestRemoveFromBasketView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")
        self.p1 = Product.objects.create(name="test product 1", price=10.00)
        self.p1.save()
        self.p2 = Product.objects.create(name="test product 2", price=20.00)
        self.p2.save()
        # Add two products
        self.basket = self.c.post(
            "/basket/add/",
            {"productId": 1, "action": "post"},
        )
        self.basket = self.c.post(
            "/basket/add/",
            {"productId": 2, "action": "post"},
        )

    def test_view_url_json_response(self):
        self.basket = self.c.post(
            "/basket/remove/",
            {"productId": 1, "action": "post"},
        )
        response = self.basket
        # Only product 2 should remain
        self.assertEqual(
            response.json(),
            {
                "product removed": "1",
                "basket quantity": 1,
                "basket subtotal": "20.00",
            },
        )

    def test_http_get_redirects(self):
        response = self.c.get("/basket/remove/")
        self.assertRedirects(response, reverse("products:all_products"))


class TestBasketClass(TestCase):
    def setUp(self):
        # Generate a request object
        request = HttpRequest()
        # Generate a session object
        session = self.client.session
        # Assign the session to the request
        request.session = session
        # Create an instance of the Basket class
        self.b = Basket(request)

        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")
        self.p1 = Product.objects.create(name="test product 1", price=10.00)
        self.p1.save()
        self.p2 = Product.objects.create(name="test product 2", price=20.00)
        self.p2.save()
        # Add two products
        self.basket = self.c.post(
            "/basket/add/",
            {"productId": 1, "action": "post"},
        )
        self.basket = self.c.post(
            "/basket/add/",
            {"productId": 2, "action": "post"},
        )

    def test_basket_class_is_iterable(self):
        """Current adding and removing tests to not meet coverage for
        the basket class' '__iter__' method. This test is designed to
        test for the presence of such a method.

        As the basket is tied to Django sessions, the set up instantiates
        a request object that has session data.
        """
        self.assertTrue(hasattr(self.b, "__iter__"))

    def test_print_basket_method(self):
        response = self.c.get("/basket/print/")
        self.assertEqual(
            response.json(), {"basket subtotal": "30.00", "delivery charge": 0}
        )

    def test_clear_session_method(self):
        response = self.b.clear_session()
        self.assertEqual(response, None)
