from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm
from .mixins import ProductOwnerMixin
from .models import Category, Product
from .services import get_cached_products


class HomeView(ListView):
    """
    CBV для отображения домашней страницы со списком продуктов.

    Показывает только опубликованные продукты.
    Использует низкоуровневое кеширование.
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Получение queryset с использованием низкоуровневого кеширования.

        Returns:
            QuerySet: Отфильтрованный queryset с опубликованными продуктами
        """
        return get_cached_products()


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    CBV для отображения детальной информации о товаре.

    Требует аутентификации пользователя.
    Использует кеширование страницы.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    login_url = "/users/login/"

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, *args, **kwargs):
        """
        Обработка запроса с кешированием.

        Args:
            *args: Аргументы запроса
            **kwargs: Ключевые аргументы запроса

        Returns:
            HttpResponse: Ответ с кешированием
        """
        return super().dispatch(*args, **kwargs)


class ContactsView(TemplateView):
    """
    CBV для отображения страницы контактов.

    Доступно всем пользователям (включая анонимных).
    """

    template_name = "catalog/contacts.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    CBV для создания нового продукта.

    Требует аутентификации пользователя.
    Автоматически устанавливает владельца.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"

    def get_form_kwargs(self):
        """
        Получение аргументов для формы.

        Returns:
            dict: Аргументы для формы, включая пользователя
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Обработка валидной формы.

        Args:
            form: Валидная форма

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        messages.success(self.request, "Продукт успешно создан!")
        # Инвалидация кеша при создании нового продукта
        if settings.CACHE_ENABLED:
            cache.delete("categories_products")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerMixin, UpdateView):
    """
    CBV для редактирования существующего продукта.

    Требует аутентификации пользователя и прав владельца.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = "/users/login/"

    def get_form_kwargs(self):
        """
        Получение аргументов для формы.

        Returns:
            dict: Аргументы для формы, включая пользователя
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного редактирования.

        Returns:
            str: URL для перенаправления на страницу продукта
        """
        messages.success(self.request, "Продукт успешно обновлен!")
        # Инвалидация кеша при обновлении продукта
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{self.object.pk}")
            cache.delete("categories_products")
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, ProductOwnerMixin, DeleteView):
    """
    CBV для удаления продукта.

    Требует аутентификации пользователя и прав владельца или модератора.
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"

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
        product_id = self.get_object().pk
        response = super().delete(request, *args, **kwargs)

        messages.success(self.request, "Продукт успешно удален!")
        # Инвалидация кеша при удалении продукта
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{product_id}")
            cache.delete("categories_products")

        return response


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    CBV для отмены публикации продукта.

    Требует права can_unpublish_product.
    """

    model = Product
    fields = []
    template_name = "catalog/product_confirm_unpublish.html"
    login_url = "/users/login/"

    def test_func(self):
        """
        Проверка прав пользователя на отмену публикации.

        Returns:
            bool: True если пользователь имеет право, иначе False
        """
        return self.request.user.has_perm("catalog.can_unpublish_product")

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

        messages.success(self.request, "Публикация продукта отменена!")
        # Инвалидация кеша при отмене публикации
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{self.object.pk}")
            cache.delete("categories_products")

        return super().form_valid(form)

    def get_success_url(self):
        """
        Получение URL для перенаправления после отмены публикации.

        Returns:
            str: URL для перенаправления на страницу продукта
        """
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class CategoryProductsView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class CategoriesListView(ListView):
    """Отображение списка всех категорий"""

    model = Category
    template_name = "catalog/categories_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)
