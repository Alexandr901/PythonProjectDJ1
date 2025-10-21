class ProductOwnerMixin:
    """Проверяет, что пользователь является владельцем товара."""

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект товара
        obj = self.get_object()
        # Проверяем, что текущий пользователь - владелец
        if obj.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
