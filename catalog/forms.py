from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.

    Включает валидацию на запрещенные слова и проверку цены.
    Автоматически устанавливает владельца при создании.
    """

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино',
        'криптовалюта',
        'крипта',
        'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    class Meta:
        """Метаданные формы."""

        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением CSS классов.

        Args:
            *args: Аргументы формы
            **kwargs: Ключевые аргументы формы
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Добавляем CSS классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'image' and field_name != 'is_published':
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

        # Для чекбокса добавляем отдельный класс
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs['class'] = 'form-check-input'

    def clean_name(self):
        """
        Валидация названия на запрещенные слова.

        Returns:
            str: Оригинальное название, если валидация прошла

        Raises:
            forms.ValidationError: Если название содержит запрещенные слова
        """
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(
                    f'Название содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """
        Валидация описания на запрещенные слова.

        Returns:
            str: Оригинальное описание, если валидация прошла

        Raises:
            forms.ValidationError: Если описание содержит запрещенные слова
        """
        description = self.cleaned_data['description'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """
        Валидация цены - не может быть отрицательной.

        Returns:
            decimal.Decimal: Цена, если валидация прошла

        Raises:
            forms.ValidationError: Если цена отрицательная
        """
        price = self.cleaned_data['price']

        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')

        return price

    def save(self, commit=True):
        """
        Сохранение формы с автоматической установкой владельца.

        Args:
            commit: Флаг сохранения в базу данных

        Returns:
            Product: Сохраненный объект продукта
        """
        instance = super().save(commit=False)

        # Устанавливаем владельца при создании
        if self.user and not instance.pk:
            instance.owner = self.user

        if commit:
            instance.save()

        return instance

