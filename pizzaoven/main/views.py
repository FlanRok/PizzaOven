from django.shortcuts import render, redirect
from catalog.models import Pizza
from django.contrib import messages

from .models import GalleryImage
from .forms import ContactForm

# Create your views here.
def index(request):
    context = {
        'new_pizzas': Pizza.objects.filter(is_new=True)[:4]
    }
    return render(request, "main/index.html", context)

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()
    return render(request, 'main/contacts.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

def gallery(request):
    images = GalleryImage.objects.all().order_by('order')
    categories = dict(GalleryImage.CATEGORY_CHOICES)
    return render(request, 'main/gallery.html', {
        'images': images,
        'categories': categories,
    })

def delivery(request):
    return render(request, 'main/delivery.html')