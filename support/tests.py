import factory
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .forms import CustomerQueryForm
from .models import FAQ, CustomerQuery
from .forms import FAQForm, CustomerQueryForm


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


class TestFAQForm(TestCase):
    def test_clean_question(self):
        data = {"question": "too short"}
        form = FAQForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please provide a longer title (minimum 10 characters).",
            form.errors["question"],
        )
        self.assertTrue(form.data["question"] == "too short")

    def test_clean_answer(self):
        data = {"answer": "too short"}
        form = FAQForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please write 20 or more characters in your answer.",
            form.errors["answer"],
        )
        self.assertTrue(form.data["answer"] == "too short")

    def test_form_is_valid(self):
        data = {
            "question": "a long enough question",
            "answer": "a long enough answer to the question",
        }
        form = FAQForm(data=data)
        self.assertTrue(form.is_valid())


class TestCustomerQueryForm(TestCase):
    def test_clean_query(self):
        data = {"query": "too short"}
        form = CustomerQueryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please provide some more detail before submitting your query"
            " (at least 20 characters).",
            form.errors["query"],
        )
        self.assertTrue(form.data["query"] == "too short")

    def test_form_is_valid(self):
        data = {"query": "here is my detailed long enough query"}
        form = CustomerQueryForm(data)
        self.assertTrue(form.is_valid())
