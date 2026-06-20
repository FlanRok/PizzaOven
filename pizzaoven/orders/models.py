from django.db import models
from catalog.models import Pizza
from users.models import User
# Create your models here.
class Order(models.Model):
    class Status(models.TextChoices):
        PROCESSING = 'processing', 'В обработке'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменён'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличными при получении'
        CARD = 'card', 'Картой при получении'
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая сумма")
    status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.PROCESSING,
    verbose_name="Статус",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name="Способ оплаты"
    )
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")
    
    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, verbose_name="Пицца")
    size = models.CharField(max_length=2, choices=[('30', '30 см'), ('35', '35 см'), ('40', '40 см')], verbose_name="Размер")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"  

    def __str__(self):
        return f"{self.pizza.name} ({self.size}см) x{self.quantity}"