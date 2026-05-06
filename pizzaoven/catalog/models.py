from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Pizza(models.Model):

    name = models.CharField(max_length=200, verbose_name="Название пиццы")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    price_30 = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена 30 см")
    price_35 = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена 35 см")
    price_40 = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена 40 см")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pizzas', verbose_name="Категория")
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2,verbose_name="Скидка в %")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_spicy = models.BooleanField(default=False, verbose_name="Острая")
    is_vegetarian = models.BooleanField(default=False, verbose_name="Вегетарианская")
    image_url = models.URLField(blank=True, verbose_name="URL изображения")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        verbose_name = "Пицца"
        verbose_name_plural = "Пиццы"
        ordering = ['order', 'name']
    
    def sell_price_30(self):
        if self.discount:
            return round(self.price_30 - self.price_30*self.discount/100, 2)
        return self.price_30
    
    def sell_price_35(self):
        if self.discount:
            return round(self.price_35 - self.price_35*self.discount/100, 2)
        return self.price_35
    
    def sell_price_40(self):
        if self.discount:
            return round(self.price_40 - self.price_40*self.discount/100, 2)
        return self.price_40

    def __str__(self):
        return self.name