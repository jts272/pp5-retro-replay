from django.test import TestCase
import factory
from .models import Order


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    name = "Joe"
    created = "24/08/2023"


# Create your tests here.
class TestOrderModel(TestCase):
    def test_order_str_method(self):
        self.order = OrderFactory()
        self.assertEqual(self.order.__str__(), "Joe's order on 24/08/2023")
