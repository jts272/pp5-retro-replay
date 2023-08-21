from django.urls import path

from . import views

app_name = "support"
urlpatterns = [
    path("", views.support, name="support"),
    path("faqs/add/", views.AddFAQ.as_view(), name="add_faq"),
    path(
        "faqs/<int:pk>/update/", views.UpdateFAQ.as_view(), name="update_faq"
    ),
    path(
        "faqs/<int:pk>/delete/", views.DeleteFAQ.as_view(), name="delete_faq"
    ),
]
