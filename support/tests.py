from django.test import TestCase
from .models import FAQ, CustomerQuery

import factory


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
