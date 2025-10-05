from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """
    CBV для отображения домашней страницы с списком продуктов.

    Доступно всем пользователям (включая анонимных).
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    CBV для отображения детальной информации о товаре.

    Требует аутентификации пользователя.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    login_url = "/users/login/"
    redirect_field_name = "next"


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
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"
    redirect_field_name = "next"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    CBV для редактирования существующего продукта.

    Требует аутентификации пользователя.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = "/users/login/"
    redirect_field_name = "next"

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного редактирования.

        Returns:
            str: URL для перенаправления на страницу продукта
        """
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    CBV для удаления продукта.

    Требует аутентификации пользователя.
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    login_url = "/users/login/"
    redirect_field_name = "next"
