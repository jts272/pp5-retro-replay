from django.test import TestCase

from . import views
from .models import Category, Product, Platform, Region


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


class TestPlatformModel(TestCase):
    def setUp(self):
        self.p = Platform.objects.create(name="test platform", slug="test-slug")

    def test_product_str_method(self):
        self.assertEqual(self.p.__str__(), "test platform")


class TestRegionModel(TestCase):
    def setUp(self):
        self.r = Region.objects.create(name="test region", slug="test-region")

    def test_region_str_method(self):
        self.assertEqual(self.r.__str__(), "test region")


class TestAllProductsView(TestCase):
    def test_view_url_200_response(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestProductsByCategoryView(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test category", slug="test-category")

    def test_view_url_200_response(self):
        response = self.client.get("/categories/test-category/")
        self.assertEqual(response.status_code, 200)


class TestProductsByPlatformView(TestCase):
    def setUp(self):
        self.p = Platform.objects.create(name="test platform", slug="test-platform")

    def test_view_url_200_response(self):
        response = self.client.get("/platforms/test-platform/")
        self.assertEqual(response.status_code, 200)


class TestProductsByRegionView(TestCase):
    def setUp(self):
        self.r = Region.objects.create(name="test region", slug="test-region")

    def test_view_url_200_response(self):
        response = self.client.get("/regions/test-region/")
        self.assertEqual(response.status_code, 200)


class TestProductDetailView(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name="test product", price=10.00)

    def test_view_url_200_response(self):
        response = self.client.get("/products/1/")
        self.assertEqual(response.status_code, 200)
