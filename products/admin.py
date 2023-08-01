from django.contrib import admin

from .models import Category, Platform, Product, Region


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class PlatformModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class RegionModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product)
admin.site.register(Platform, PlatformModelAdmin)
admin.site.register(Region, RegionModelAdmin)
