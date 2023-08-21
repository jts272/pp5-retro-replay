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
    MAX_CHARS = 1000
    sender = models.EmailField(
        help_text="Reply to your customer at this address."
    )
    query = models.CharField(
        max_length=MAX_CHARS,
        help_text=(
            f"Please outline your query in less than {MAX_CHARS} characters."
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    replied = models.BooleanField(
        default=False,
        help_text=(
            "Keep track of which customer queries you have replied to."
        ),
    )
    resolved = models.BooleanField(
        default=False,
        help_text=(
            "Mark as resolved when your customer query has been dealt with."
        ),
    )

    class Meta:
        verbose_name_plural = "Customer queries"

    def __str__(self):
        return f"Query on {self.created} from {self.sender}"
