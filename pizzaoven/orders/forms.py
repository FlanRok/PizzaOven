from django import forms
import re

class OrderForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        min_length=5,
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
                'Введите корректный номер телефона в формате'
            )
        
        return cleaned