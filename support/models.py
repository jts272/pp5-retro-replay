from django.db import models


# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(
        default=True,
        help_text="Mark as published to make the FAQ visible on the site.",
    )

    class Meta:
        verbose_name = "FAQ"

    def __str__(self):
        return self.question


class CustomerQuery(models.Model):
    sender = models.EmailField(
        help_text="Reply to your customer at this address."
    )
    query = models.CharField(
        max_length=400,
        help_text=(
            "Please outline your query for us in less than 400 characters."
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    replied = models.BooleanField(
        default=False,
        help_text=(
            "Keep track of which customer queries you have replied to.",
        ),
    )

    class Meta:
        verbose_name_plural = "Customer queries"

    def __str__(self):
        return f"Query on {self.created} from {self.sender}"
