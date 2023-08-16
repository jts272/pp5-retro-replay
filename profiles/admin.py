from django.contrib import admin

from .models import Address, Profile


class AddressModelAdmin(admin.ModelAdmin):
    readonly_fields = ["uuid"]


# Register your models here.
admin.site.register(Address, AddressModelAdmin)
admin.site.register(Profile)
