from django import forms
from .models import Order
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'address',
            'phone',
            'comment',
            'payment_method'
        ]
    def clean_address(self):
        address = self.cleaned_data['address']
        address = address.strip()

        if len(address) < 10:
            raise forms.ValidationError(
                "Адрес должен содержать минимум 10 символов"
            )

        if not re.search(r'[а-яА-Яa-zA-Z]', address):
            raise forms.ValidationError(
                "Адрес должен содержать название улицы или города"
            )

        if not re.search(r'\d', address):
            raise forms.ValidationError(
                "Укажите номер дома"
            )

        if not re.match(
            r'^[а-яА-Яa-zA-Z0-9\s.,\-]+$',
            address
        ):
            raise forms.ValidationError(
                "Адрес содержит недопустимые символы"
            )

        return address
    address = forms.CharField(
        max_length=255,
        label='Адрес доставки',
        widget=forms.TextInput(attrs={'placeholder': 'Введите адрес'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'})
    )
    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите дополнительный комментарий'})
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        if cleaned.startswith('8') and len(cleaned) == 11:
            cleaned = '+7' + cleaned[1:]
        elif cleaned.startswith('7') and len(cleaned) == 11:
            cleaned = '+' + cleaned
        
        if not re.match(r'^\+\d{11}$', cleaned):
            raise forms.ValidationError(
                'Введите корректный номер телефона'
            )
        
        return cleaned