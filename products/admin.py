from django.contrib import admin

from .models import Category, Platform, Product, Region


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "region", "platform", "category", "price"]
    search_fields = [
        "name",
        "region__name",
        "platform__name",
        "category__name",
        "price",
        "pk",
    ]
    readonly_fields = ["slug"]


class PlatformModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class RegionModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Platform, PlatformModelAdmin)
admin.site.register(Region, RegionModelAdmin)
