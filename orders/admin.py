import json
from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'address', 'display_basket_history', 'created', 'status', 'initiator')
    readonly_fields = ('display_basket_history',)

    def display_basket_history(self, obj):
        basket_history = json.loads(obj.basket_history)
        print(basket_history)
        return ", ".join([f"{key}: {value}" for key, value in basket_history.items()])

    display_basket_history.short_description = "Basket History"

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if obj:
            fields.remove('basket_history')
            fields.append('display_basket_history')
            fields.remove('display_basket_history')
        return fields


admin.site.register(Order, OrderAdmin)

