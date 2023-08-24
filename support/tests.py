import factory
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .forms import CustomerQueryForm
from .models import FAQ, CustomerQuery


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    question = "question"


class CustomerQueryFactory(factory.Factory):
    class Meta:
        model = CustomerQuery

    sender = "test@mail.com"
    created = "24/08/2023"


# Create your tests here.
class TestFAQModel(TestCase):
    def test_faq_str_method(self):
        self.f = FAQFactory()
        self.assertEqual(self.f.__str__(), "question")


class TestCustomerQuery(TestCase):
    def test_customer_query_str_method(self):
        self.q = CustomerQueryFactory()
        self.assertEqual(
            self.q.__str__(), "Query on 24/08/2023 from test@mail.com"
        )


class TestSupportViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="secret"
        )
        self.user.save()
        self.c = Client()
        self.c.login(username="tester", password="secret")

    def test_support_view_url_200(self):
        response = self.c.get("/support/")
        self.assertEqual(response.status_code, 200)

    def test_not_form_is_valid(self):
        form = CustomerQueryForm(
            data={
                "query": "@",
            }
        )
        self.assertFalse(form.is_valid())
