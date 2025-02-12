import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from users.models import CustomUser
from cart.models import CartItem


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    first_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True)

    def get_user_carts(self, username):
        baskets = CartItem.objects.filter(user=username)
        return baskets

    def update_after_payment(self, username):
        baskets = CartItem.objects.filter(user=username)
        baskets_history = {}
        for basket in baskets:
            baskets_history[basket.product.name] = str(basket.product.price)
        self.status = self.PAID
        self.basket_history = json.dumps(baskets_history, cls=DjangoJSONEncoder)
        self.initiator = username
        self.save()

    def get_basket_history_display(self):
        basket_history = json.loads(self.basket_history)
        return basket_history

    def __str__(self):
        return f'order: {self.first_name}'
