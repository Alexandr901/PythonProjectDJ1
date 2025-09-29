from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'image':  # Для image уже задан класс
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(
                    f'Название содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data['description'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены - не может быть отрицательной"""
        price = self.cleaned_data['price']

        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')

        return price
