from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категории продуктов."""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        """Метаданные модели категории."""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Строковое представление категории.

        Returns:
            str: Название категории
        """
        return self.name


class Product(models.Model):
    """Модель продукта."""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/", verbose_name="Изображение", null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        """Метаданные модели продукта."""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        """
        Строковое представление продукта.

        Returns:
            str: Название продукта
        """
        return self.name

    def short_description(self):
        """
        Возвращает сокращенное описание.

        Returns:
            str: Сокращенное описание (первые 100 символов)
        """
        if len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description
