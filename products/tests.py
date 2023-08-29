from django.test import TestCase
from django.urls import reverse

from .models import Category, Platform, Product, Region


# Create your tests here.
class TestCategoryModel(TestCase):
    def setUp(self):
        self.c = Category.objects.create(
            name="test category", slug="test-category"
        )

    def test_category_str_method(self):
        self.assertEqual(self.c.__str__(), "test category")


class TestProductModel(TestCase):
    def setUp(self):
        self.platform = Platform.objects.create(
            name="test platform", slug="test-platform"
        )
        self.region = Region.objects.create(
            name="test region", slug="test-region"
        )
        self.p = Product.objects.create(
            name="test product",
            price=10.00,
            platform=self.platform,
            region=self.region,
        )

    def test_product_str_method(self):
        self.assertEqual(
            self.p.__str__(), "test product for test platform - test region"
        )

    def test_product_mark_as_sold_method(self):
        self.p.mark_as_sold()
        self.assertTrue(self.p.sold)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.p.get_absolute_url(), "/products/view/test-product/"
        )


class TestPlatformModel(TestCase):
    def setUp(self):
        self.p = Platform.objects.create(
            name="test platform", slug="test-slug"
        )

    def test_product_str_method(self):
        self.assertEqual(self.p.__str__(), "test platform")


class TestRegionModel(TestCase):
    def setUp(self):
        self.r = Region.objects.create(name="test region", slug="test-region")

    def test_region_str_method(self):
        self.assertEqual(self.r.__str__(), "test region")


class TestAllProductsView(TestCase):
    def test_view_url_200_response(self):
        response = self.client.get("/products/all-products/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get("/products/all-products/", {"q": "test"})
        self.assertEqual(response.status_code, 200)


class TestSoldProductsView(TestCase):
    def test_view_url_200_response(self):
        response = self.client.get("/products/sold-products/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get("/products/sold-products/", {"q": "test"})
        self.assertEqual(response.status_code, 200)


class TestProductsByCategoryView(TestCase):
    def setUp(self):
        self.c = Category.objects.create(
            name="test category", slug="test-category"
        )

    def test_view_url_200_response(self):
        response = self.client.get("/products/categories/test-category/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get(
            "/products/categories/test-category/", {"q": "test"}
        )
        self.assertEqual(response.status_code, 200)


class TestProductsByPlatformView(TestCase):
    def setUp(self):
        self.p = Platform.objects.create(
            name="test platform", slug="test-platform"
        )

    def test_view_url_200_response(self):
        response = self.client.get("/products/platforms/test-platform/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get(
            "/products/platforms/test-platform/", {"q": "test"}
        )
        self.assertEqual(response.status_code, 200)


class TestProductsByRegionView(TestCase):
    def setUp(self):
        self.r = Region.objects.create(name="test region", slug="test-region")

    def test_view_url_200_response(self):
        response = self.client.get("/products/regions/test-region/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get(
            "/products/regions/test-region/", {"q": "test"}
        )
        self.assertEqual(response.status_code, 200)


class TestProductDetailView(TestCase):
    def setUp(self):
        self.p = Product.objects.create(
            name="test product", price=10.00, slug="test-product"
        )

    def test_view_url_200_response(self):
        response = self.client.get("/products/view/test-product/")
        self.assertEqual(response.status_code, 200)

    def test_search_200_response(self):
        response = self.client.get("/products/all-products/", {"q": "test"})
        self.assertEqual(response.status_code, 200)
