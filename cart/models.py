from django.db import models
from products.models import Product
from users.models import CustomUser


class CartItem(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Корзина для {self.user} | Продукт: {self.product.name}'

