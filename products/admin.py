from django.contrib import admin

from .models import Category, Product


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


# Register your models here.
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product)
