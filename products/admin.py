from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Platform, Product, Region


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class ProductModelAdmin(SummernoteModelAdmin):
    list_display = [
        "pk",
        "name",
        "category",
        "platform",
        "region",
        "price",
        "sold",
    ]
    search_fields = [
        "name",
        "region__name",
        "platform__name",
        "category__name",
        "price",
        "pk",
    ]
    readonly_fields = ["slug", "created", "updated"]
    summernote_fields = ["description"]


class PlatformModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class RegionModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Platform, PlatformModelAdmin)
admin.site.register(Region, RegionModelAdmin)
