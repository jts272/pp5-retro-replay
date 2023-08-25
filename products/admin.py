from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Platform, Product, Region


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


@admin.action(description="Mark selected products as visible")
def make_product_visible(modeladmin, request, queryset):
    queryset.update(visible=True)


@admin.action(description="Mark selected products as invisible")
def make_product_invisible(modeladmin, request, queryset):
    queryset.update(visible=False)


@admin.action(description="Mark selected products as available for sale")
def make_product_for_sale(modeladmin, request, queryset):
    queryset.update(sold=False)


@admin.action(description="Mark selected products as unavailable for sale")
def make_product_sold(modeladmin, request, queryset):
    queryset.update(sold=True)


class ProductModelAdmin(SummernoteModelAdmin):
    # Product id can be sorted in list display, unlike PK
    list_display = [
        "name",
        "category",
        "platform",
        "region",
        "price",
        "created",
        "updated",
        "visible",
        "sold",
    ]
    search_fields = [
        "name",
        "region__name",
        "platform__name",
        "category__name",
        "price",
        "id",
    ]
    readonly_fields = ["slug", "created", "updated"]
    summernote_fields = ["description"]
    actions = [
        make_product_visible,
        make_product_invisible,
        make_product_for_sale,
        make_product_sold,
    ]


class PlatformModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class RegionModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Platform, PlatformModelAdmin)
admin.site.register(Region, RegionModelAdmin)
