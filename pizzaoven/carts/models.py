from django.db import models
from catalog.models import Pizza
from users.models import User

# Create your models here.

class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.pizzas_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    SIZE_CHOICES = [
        ('30', '30 см'),
        ('35', '35 см'),
        ('40', '40 см'),
    ]
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    pizza = models.ForeignKey(to=Pizza, on_delete=models.CASCADE, verbose_name="Пицца")
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='30', verbose_name="Размер")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    
    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
    
    objects = CartQuerySet().as_manager()

    def get_price(self):
        if self.size == '30':
            return self.pizza.sell_price_30()
        elif self.size == '35':
            return self.pizza.sell_price_35()
        elif self.size == '40':
            return self.pizza.sell_price_40()
        return self.pizza.sell_price_30()
    
    def pizzas_price(self):
        return round(self.get_price() * self.quantity, 2)
    
    def __str__(self):
        return f"Корзина {self.user.username} | Пицца {self.pizza.name} | Количество {self.quantity}"