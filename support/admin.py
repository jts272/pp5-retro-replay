from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQ


class FAQAdmin(SummernoteModelAdmin):
    fields = ["question", "answer", "created", "updated", "published"]
    list_display = ["question", "created", "updated", "published"]
    summernote_fields = ["answer"]
    readonly_fields = ["created", "updated"]


# Register your models here.
admin.site.register(FAQ, FAQAdmin)
