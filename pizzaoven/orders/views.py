from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from carts.models import Cart
from .models import Order, OrderItem

@login_required
def order_create(request):
    carts = Cart.objects.filter(user=request.user)
    if not carts.exists():
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', '')

        if not address or not phone:
            messages.error(request, "Заполните адрес и телефон")
            return render(request, 'orders/order_form.html', {'carts': carts})

        total_price = carts.total_price()
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=address,
            phone=phone,
            comment=comment
        )
        for cart_item in carts:
            OrderItem.objects.create(
                order=order,
                pizza=cart_item.pizza,
                size=cart_item.size,
                quantity=cart_item.quantity,
                price=cart_item.get_price()
            )
        carts.delete()
        messages.success(request, f"Заказ #{order.id} успешно оформлен!")
        return redirect('profile')

    return render(request, 'orders/order_form.html', {'carts': carts})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})