from django.contrib import admin

from .models import Category, Platform, Product


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class PlatformModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product)
admin.site.register(Platform, PlatformModelAdmin)
