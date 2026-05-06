from django.contrib import admin
from catalog.models import Category, Pizza

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_30', 'price_35', 'price_40', 'is_popular', 'is_new', 'order', 'discount')
    list_editable = ('order', 'is_popular', 'is_new', 'discount')
    list_filter = ('category', 'is_popular', 'is_new', 'is_spicy', 'is_vegetarian')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}