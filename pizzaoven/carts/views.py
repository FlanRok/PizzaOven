from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Pizza
from carts.models import Cart

# Create your views here.

def cart(request):
    carts = Cart.objects.filter(user=request.user)
    context = {
        'carts': carts
    }
    return render(request, "carts/cart.html", context)

def cart_add(request, pizza_slug):
    pizza = Pizza.objects.get(slug=pizza_slug)
    size = request.POST.get('size')
    if size not in ['30', '35', '40']:
        size = '30'

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            pizza=pizza,
            size=size,
            defaults={'quantity': 0}
        )
        cart.quantity += 1
        cart.save()

        total_quantity = sum(c.quantity for c in Cart.objects.filter(user=request.user))

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'total_quantity': total_quantity,
                'cart_id': cart.id,
                'message': f'{pizza.name} ({size} см) добавлена в корзину'
            })
        else:
            return redirect(request.META.get('HTTP_REFERER', 'cart'))
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Необходимо войти в систему'}, status=403)
        return redirect('login')

def cart_change(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Войдите в систему'}, status=403)

    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart.quantity += 1
    elif action == 'decrease':
        if cart.quantity > 1:
            cart.quantity -= 1
        else:
            cart.delete()
            carts = Cart.objects.filter(user=request.user)
            total_quantity = carts.total_quantity()
            total_price = carts.total_price()
            return JsonResponse({
                'success': True,
                'deleted': True,
                'cart_id': cart_id,
                'total_quantity': total_quantity,
                'total_price': total_price,
            })
    else:
        return JsonResponse({'success': False, 'message': 'Неверное действие'}, status=400)

    cart.save()

    carts = Cart.objects.filter(user=request.user)
    total_quantity = carts.total_quantity()
    total_price = carts.total_price()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'new_quantity': cart.quantity,
            'new_item_price': cart.pizzas_price(),
            'total_quantity': total_quantity,
            'total_price': total_price,
            'cart_id': cart_id,
        })
    else:
        from django.shortcuts import redirect
        return redirect('cart')

def cart_remove(request, cart_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart.delete()
        
        carts = Cart.objects.filter(user=request.user)
        total_quantity = carts.total_quantity()
        total_price = carts.total_price()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'total_quantity': total_quantity,
                'total_price': total_price,
                'cart_id': cart_id,
            })
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Не удалось удалить'}, status=400)
    return redirect(request.META.get('HTTP_REFERER', 'cart'))