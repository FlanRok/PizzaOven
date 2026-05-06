from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('pizza', 'size', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'status', 'phone')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'total_price', 'address', 'phone', 'comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_confirmed', 'mark_as_completed']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Подтвердить выбранные заказы"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Завершить выбранные заказы"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'pizza', 'size', 'quantity', 'price')
    list_filter = ('size',)
    search_fields = ('order__id', 'pizza__name')
    readonly_fields = ('order', 'pizza', 'size', 'quantity', 'price')