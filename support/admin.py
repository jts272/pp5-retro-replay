from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQ, CustomerQuery


class FAQAdmin(SummernoteModelAdmin):
    fields = ["question", "answer", "created", "updated", "published"]
    list_display = ["question", "created", "updated", "published"]
    summernote_fields = ["answer"]
    readonly_fields = ["created", "updated"]


class CustomerQueryAdmin(admin.ModelAdmin):
    fields = ["sender", "query", "created", "replied", "resolved"]
    list_display = ["sender", "created", "replied", "resolved"]
    readonly_fields = ["sender", "query", "created"]


# Register your models here.
admin.site.register(FAQ, FAQAdmin)
admin.site.register(CustomerQuery, CustomerQueryAdmin)
