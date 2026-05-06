from django.shortcuts import render
from .models import Pizza,Category

# Create your views here.
def catalog(request):
    pizzas = Pizza.objects.all()
    categories = Category.objects.all()
    context = {
        'pizzas': pizzas,
        'categories': categories,
    }
    return render(request, 'catalog/catalog.html', context)
