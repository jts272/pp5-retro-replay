from django.test import TestCase

from .models import Category, Product


# Create your tests here.
class TestCategoryModel(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test category", slug="test-category")

    def test_category_str_method(self):
        self.assertEqual(self.c.__str__(), "test category")


class TestProductModel(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="test product", price=10.00)

    def test_product_str_method(self):
        self.assertEqual(self.p.__str__(), "test product")
