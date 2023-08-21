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
