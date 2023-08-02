from django.test import TestCase


# Create your tests here.
class TestHomeView(TestCase):
    def test_view_url_200_response(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
