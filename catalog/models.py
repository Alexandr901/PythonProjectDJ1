from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Модель продукта с владельцем и статусом публикации.

    Attributes:
        name: Название продукта
        description: Описание продукта
        image: Изображение продукта
        category: Категория продукта
        price: Цена продукта
        created_at: Дата создания
        updated_at: Дата последнего обновления
        is_published: Статус публикации
        owner: Владелец продукта
    """

    # Статусы публикации
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Черновик')),
        (STATUS_PUBLISHED, _('Опубликовано')),
        (STATUS_ARCHIVED, _('В архиве')),
    ]

    name = models.CharField(max_length=100, verbose_name=_('Наименование'))
    description = models.TextField(verbose_name=_('Описание'))
    image = models.ImageField(
        upload_to='products/',
        verbose_name=_('Изображение'),
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name=_('Категория')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Цена за покупку')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата последнего изменения')
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Опубликовано')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('Владелец'),
        null=True,
        blank=True,
        related_name='products'
    )

    class Meta:
        """Метаданные модели продукта."""

        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        permissions = [
            ('can_unpublish_product', _('Может отменять публикацию продукта')),
            ('can_change_published_status', _('Может менять статус публикации')),
        ]

    def __str__(self):
        """
        Строковое представление продукта.

        Returns:
            str: Название продукта
        """
        return self.name

    def get_absolute_url(self):
        """
        Получение абсолютного URL для продукта.

        Returns:
            str: URL детальной страницы продукта
        """
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

    def short_description(self):
        """
        Возвращает сокращенное описание.

        Returns:
            str: Сокращенное описание (первые 100 символов)
        """
        if len(self.description) > 100:
            return self.description[:100] + '...'
        return self.description


class Category(models.Model):
    """Модель категории продуктов."""

    name = models.CharField(max_length=100, verbose_name=_('Наименование'))
    description = models.TextField(verbose_name=_('Описание'))

    class Meta:
        """Метаданные модели категории."""

        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        """
        Строковое представление категории.

        Returns:
            str: Название категории
        """
        return self.name
