import os
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image','category', 'price']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите наименование товара'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте подробное описание товара'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '0.00'
        })

    def validate_forbidden_words(self, text):
        """Вспомогательный метод для поиска запрещенных слов (без учета регистра)."""
        if text:
            text_lower = text.lower()
            for word in self.forbidden_words:
                if word in text_lower:
                    raise forms.ValidationError(f'Использование слова "{word}" запрещено!')
        return text

    def clean_name(self):
        """Валидация поля наименования товара."""
        name = self.cleaned_data.get('name')
        return self.validate_forbidden_words(name)

    def clean_description(self):
        """Валидация поля описания товара."""
        description = self.cleaned_data.get('description')
        return self.validate_forbidden_words(description)

    def clean_price(self):
        """Валидация поля цены товара."""
        price = self.cleaned_data.get('price')

        # Проверка, что цена не отрицательная
        if price is not None and price < 0:
            raise forms.ValidationError('Цена товара не может быть отрицательной!')

        return price

    def clean_image(self):
        """Валидация формата и размера изображения."""
        image = self.cleaned_data.get('image')

        # Если картинка не была загружена, возвращаем None
        if not image:
            return image

        # Проверка размера файла (максимум 5 МБ)
        max_size = 5 * 1024 * 1024  # в байтах
        if image.size > max_size:
            raise forms.ValidationError('Размер файла не должен превышать 5 МБ!')

        # Проверка расширения файла (только JPEG, JPG или PNG)
        file_extension = os.path.splitext(image.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if file_extension not in valid_extensions:
            raise forms.ValidationError('Допускаются только файлы форматов JPEG и PNG!')

        return image
