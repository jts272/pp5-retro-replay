from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["product", "price"]
    # Don't include extra blank placeholder entries
    extra = 0


class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "name",
        "amount",
        "created",
        "updated",
        "paid",
    ]
    inlines = [OrderItemInline]


# Register your models here.
admin.site.register(Order, OrderModelAdmin)
admin.site.register(OrderItem)
