from django.conf import settings
from django.core.cache import cache

from .models import Category, Product


def get_cached_products():
    """
    Получение списка продуктов с низкоуровневым кешированием.

    Returns:
        QuerySet: Список опубликованных продуктов
    """
    if settings.CACHE_ENABLED:
        key = "all_published_products"
        products = cache.get(key)
        if products is not None:
            return products

        # Получаем продукты из базы данных
        products = Product.objects.filter(is_published=True).select_related(
            "category", "owner"
        )

        # Сохраняем в кеш на 10 минут
        cache.set(key, products, 60 * 10)
        return products
    else:
        return Product.objects.filter(is_published=True).select_related(
            "category", "owner"
        )


def get_cached_categories():
    """
    Получение списка категорий с низкоуровневым кешированием.

    Returns:
        QuerySet: Список всех категорий
    """
    if settings.CACHE_ENABLED:
        key = "all_categories"
        categories = cache.get(key)
        if categories is not None:
            return categories

        # Получаем категории из базы данных
        categories = Category.objects.all()

        # Сохраняем в кеш на 1 час
        cache.set(key, categories, 60 * 60)
        return categories
    else:
        return Category.objects.all()


def invalidate_products_cache():
    """
    Инвалидация кеша продуктов.

    Вызывается при изменении продуктов.
    """
    if settings.CACHE_ENABLED:
        cache_keys = ["all_published_products", "all_categories", "categories_products"]

        # Удаляем все связанные ключи кеша
        for key in cache_keys:
            cache.delete(key)

        # Также удаляем кеш для отдельных категорий
        categories = Category.objects.all()
        for category in categories:
            cache.delete(f"category_products_{category.slug}")
