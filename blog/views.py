from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import BlogPost


class BlogPostListView(ListView):
    """CBV для отображения списка опубликованных блоговых записей."""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """
        Получение queryset с фильтрацией по опубликованным записям.

        Returns:
            QuerySet: Отфильтрованный queryset с опубликованными записями
        """
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """CBV для отображения детальной информации о блоговой записи."""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """
        Получение объекта с увеличением счетчика просмотров.

        Args:
            queryset: Базовый queryset для поиска объекта

        Returns:
            BlogPost: Объект блоговой записи
        """
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    """CBV для создания новой блоговой записи."""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    """CBV для редактирования блоговой записи."""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного редактирования.

        Returns:
            str: URL для перенаправления на страницу записи
        """
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """CBV для удаления блоговой записи."""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
