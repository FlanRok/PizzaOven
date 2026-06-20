from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from carts.models import Cart
from .models import Order, OrderItem
from .forms import OrderForm

@login_required
def order_create(request):
    carts = Cart.objects.filter(user=request.user)
    if not carts.exists():
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data.get('comment', '') 
            payment_method = form.cleaned_data['payment_method']

            total_price = carts.total_price()
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                address=address,
                phone=phone,
                comment=comment,
                payment_method=payment_method
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
        else:
            context = {
                'carts': carts,
                'form': form,
            }
            return render(request, 'orders/order_form.html', context)
    else:
        form = OrderForm()

    context = {
        'carts': carts,
        'form': form,
    }
    return render(request, 'orders/order_form.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})