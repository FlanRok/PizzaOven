from django.contrib import admin
from .models import Cart

# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'pizza', 'quantity', 'created_timestamp')
    search_fields = ('user', 'pizza', 'quantity', 'created_timestamp')
    list_filter = ('user', 'pizza__name', 'created_timestamp')

class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "pizza", "quantity"
    search_fields = "pizza", "quantity"
    extra = 1