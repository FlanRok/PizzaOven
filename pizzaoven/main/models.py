from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    class Meta:
        verbose_name = "Сообщение с сайта"
        verbose_name_plural = "Сообщения с сайта"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение от {self.name} - {self.subject}"
    
class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('pizza', 'Пиццы'),
        ('interior', 'Интерьер'),
        ('team', 'Команда'),
        ('events', 'Акции и события'),
        ('process', 'Приготовление'),
    ]
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(upload_to='gallery/', verbose_name="Изображение")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='pizza', verbose_name="Категория")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title