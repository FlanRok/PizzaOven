from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('cart_add/<slug:pizza_slug>/', views.cart_add, name='cart_add'),
    path('cart_change/<int:cart_id>/', views.cart_change, name='cart_change'),
    path('cart_remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
]
