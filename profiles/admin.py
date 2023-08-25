from django.contrib import admin

from .models import Address, Profile


class AddressModelAdmin(admin.ModelAdmin):
    readonly_fields = ["uuid"]
    list_display = [
        "uuid",
        "profile",
        "created",
        "updated",
        "default",
    ]


# Register your models here.
admin.site.register(Address, AddressModelAdmin)
admin.site.register(Profile)
