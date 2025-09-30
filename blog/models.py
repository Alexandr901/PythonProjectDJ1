from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """Модель блоговой записи."""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog/", verbose_name="Превью", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        """Метаданные модели блоговой записи."""

        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        """
        Строковое представление блоговой записи.

        Returns:
            str: Заголовок записи
        """
        return self.title

    def get_absolute_url(self):
        """
        Получение абсолютного URL для записи.

        Returns:
            str: URL детальной страницы записи
        """
        return reverse("blog:post_detail", kwargs={"pk": self.pk})
