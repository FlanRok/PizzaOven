from .models import Cart
 
def cart_total_quantity(request):
    total_quantity = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total_quantity = sum(cart.quantity for cart in carts)
    else:
        session_key = request.session.session_key
        if session_key:
            carts = Cart.objects.filter(session_key=session_key)
            total_quantity = sum(cart.quantity for cart in carts)
    return {'cart_total_quantity': total_quantity}