from django.test import TestCase
import factory
from .models import Order, OrderItem
from products.models import Product, Platform, Region


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    name = "Joe"
    created = "24/08/2023"


class PlatformFactory(factory.Factory):
    class Meta:
        model = Platform

    name = "test platform"


class RegionFactory(factory.Factory):
    class Meta:
        model = Region

    name = "pal"


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = "test product"
    platform = PlatformFactory()
    region = RegionFactory()


class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem

    order = OrderFactory()
    product = ProductFactory()
    id = 1


# Create your tests here.
class TestOrderModel(TestCase):
    def test_order_str_method(self):
        self.order = OrderFactory()
        self.assertEqual(self.order.__str__(), "Joe's order on 24/08/2023")


class TestOrderItemModel(TestCase):
    def test_order_item_str_method(self):
        self.order_item = OrderItemFactory()
        self.assertEqual(
            self.order_item.__str__(),
            "Order Item id: 1 - Item: test product for test platform - pal",
        )
