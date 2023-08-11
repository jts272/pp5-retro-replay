from django.contrib import admin

from .models import Order


class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "name",
        "amount",
        "created",
        "updated",
        "paid",
    ]


# Register your models here.
admin.site.register(Order, OrderModelAdmin)
