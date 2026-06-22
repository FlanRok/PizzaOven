from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name="Аватар")
    orders_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
    
    def get_discount(self):
        if self.orders_count >= 30:
            return 15
        elif self.orders_count >= 15:
            return 10
        elif self.orders_count >= 5:
            return 5

        return 0