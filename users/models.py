from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Кастомная модель пользователя с email в качестве идентификатора.

    Attributes:
        email: Email пользователя (используется для входа)
        avatar: Аватар пользователя
        phone: Номер телефона
        country: Страна
    """

    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Enter a valid email address."),
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        help_text=_("Upload your profile picture"),
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone number"),
        blank=True,
        null=True,
        help_text=_("Enter your phone number"),
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        blank=True,
        null=True,
        help_text=_("Enter your country"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Метаданные модели пользователя."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["email"]

    def __str__(self):
        """
        Строковое представление пользователя.

        Returns:
            str: Email пользователя
        """
        return self.email

    def get_full_name(self):
        """
        Полное имя пользователя.

        Returns:
            str: Полное имя (имя + фамилия) или email
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        """
        Короткое имя пользователя.

        Returns:
            str: Имя или email
        """
        return self.first_name or self.email
