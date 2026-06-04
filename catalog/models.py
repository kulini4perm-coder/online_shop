from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование категории')
    description = models.TextField(verbose_name='Описание категории', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    # Статус публикации (по умолчанию скрыт)
    is_published = models.BooleanField(default=False, verbose_name='Статус публикации')

    # Поле владельца продукта
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} ({self.price})'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name', 'price']
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]

