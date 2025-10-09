from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm


class ProductOwnerMixin(UserPassesTestMixin):
    """
    Миксин для проверки прав доступа к продукту.

    Разрешает доступ владельцу продукта или модератору.
    """

    def test_func(self):
        """
        Проверка прав доступа пользователя.

        Returns:
            bool: True если пользователь имеет доступ, иначе False
        """
        product = self.get_object()
        user = self.request.user

        # Владелец имеет полный доступ
        if product.owner == user:
            return True

        # Модератор имеет доступ к удалению и отмене публикации
        if user.has_perm('catalog.delete_product') or user.has_perm('catalog.can_unpublish_product'):
            return True

        return False

    def handle_no_permission(self):
        """
        Обработка случая, когда пользователь не имеет прав доступа.

        Returns:
            HttpResponse: Ответ с перенаправлением и сообщением об ошибке
        """
        messages.error(
            self.request,
            'У вас недостаточно прав для выполнения этого действия.'
        )
        return super().handle_no_permission()


class HomeView(ListView):
    """
    CBV для отображения домашней страницы со списком продуктов.

    Показывает только опубликованные продукты.
    """

    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Получение queryset с фильтрацией по опубликованным продуктам.

        Returns:
            QuerySet: Отфильтрованный queryset с опубликованными продуктами
        """
        return Product.objects.all()


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    CBV для отображения детальной информации о товаре.

    Требует аутентификации пользователя.
    """

    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = '/users/login/'


class ContactsView(TemplateView):
    """
    CBV для отображения страницы контактов.

    Доступно всем пользователям (включая анонимных).
    """

    template_name = 'catalog/contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    CBV для создания нового продукта.

    Требует аутентификации пользователя.
    Автоматически устанавливает владельца.
    """

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def get_form_kwargs(self):
        """
        Получение аргументов для формы.

        Returns:
            dict: Аргументы для формы, включая пользователя
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Обработка валидной формы.

        Args:
            form: Валидная форма

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        messages.success(
            self.request,
            'Продукт успешно создан!'
        )
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerMixin, UpdateView):
    """
    CBV для редактирования существующего продукта.

    Требует аутентификации пользователя и прав владельца.
    """

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/users/login/'

    def get_form_kwargs(self):
        """
        Получение аргументов для формы.

        Returns:
            dict: Аргументы для формы, включая пользователя
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного редактирования.

        Returns:
            str: URL для перенаправления на страницу продукта
        """
        messages.success(
            self.request,
            'Продукт успешно обновлен!'
        )
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'pk': self.object.pk}
        )


class ProductDeleteView(LoginRequiredMixin, ProductOwnerMixin, DeleteView):
    """
    CBV для удаления продукта.

    Требует аутентификации пользователя и прав владельца или модератора.
    """

    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def delete(self, request, *args, **kwargs):
        """
        Обработка удаления продукта.

        Args:
            request: HTTP запрос
            *args: Аргументы
            **kwargs: Ключевые аргументы

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        messages.success(
            self.request,
            'Продукт успешно удален!'
        )
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    CBV для отмены публикации продукта.

    Требует права can_unpublish_product.
    """

    model = Product
    fields = []
    template_name = 'catalog/product_confirm_unpublish.html'
    login_url = '/users/login/'

    def test_func(self):
        """
        Проверка прав пользователя на отмену публикации.

        Returns:
            bool: True если пользователь имеет право, иначе False
        """
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        """
        Обработка валидной формы отмены публикации.

        Args:
            form: Валидная форма

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        self.object.is_published = False
        self.object.save()

        messages.success(
            self.request,
            'Публикация продукта отменена!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        """
        Получение URL для перенаправления после отмены публикации.

        Returns:
            str: URL для перенаправления на страницу продукта
        """
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'pk': self.object.pk}
        )

