from django import template

register = template.Library()


@register.filter
def can_edit_product(user, product):
    """
    Проверяет, может ли пользователь редактировать продукт.

    Args:
        user: Текущий пользователь
        product: Продукт для проверки

    Returns:
        bool: True если пользователь может редактировать продукт
    """
    if not user.is_authenticated:
        return False
    return product.owner == user or user.has_perm("catalog.change_product")


@register.filter
def can_delete_product(user, product):
    """
    Проверяет, может ли пользователь удалить продукт.

    Args:
        user: Текущий пользователь
        product: Продукт для проверки

    Returns:
        bool: True если пользователь может удалить продукт
    """
    if not user.is_authenticated:
        return False
    return product.owner == user or user.has_perm("catalog.delete_product")


@register.filter
def can_unpublish_product(user):
    """
    Проверяет, может ли пользователь отменять публикацию продуктов.

    Args:
        user: Текущий пользователь

    Returns:
        bool: True если пользователь имеет право отменять публикацию
    """
    if not user.is_authenticated:
        return False
    return user.has_perm("catalog.can_unpublish_product")
