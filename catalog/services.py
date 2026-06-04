from django.core.cache import cache
from .models import Product


class ProductService:

    @staticmethod
    def get_products_by_category(category_id: int):
        """Сервис для списка продуктов в категории"""
        cache_key = f'category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            products = list(Product.objects.filter(category_id=category_id, is_published=True))
            cache.set(cache_key, products, timeout=60 * 15)

        return products

    @staticmethod
    def get_all_published_products():
        """Сервис для общего списка продуктов."""
        cache_key = 'all_published_products'
        products = cache.get(cache_key)

        if products is None:
            products = list(Product.objects.filter(is_published=True))
            cache.set(cache_key, products, timeout=60 * 15)

        return products
