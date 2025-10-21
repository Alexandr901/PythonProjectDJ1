from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.

    Attributes:
        email: Email пользователя
        password1: Пароль
        password2: Подтверждение пароля
        phone: Номер телефона
        country: Страна
    """

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Enter your email")}
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Enter password")}
        ),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Confirm password")}
        ),
    )
    phone = forms.CharField(
        label=_("Phone number"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter phone number")}
        ),
    )
    country = forms.CharField(
        label=_("Country"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter country")}
        ),
    )

    class Meta:
        """Метаданные формы регистрации."""

        model = User
        fields = ["email", "password1", "password2", "phone", "country"]

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением CSS классов.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                field.widget.attrs.get("class", "") + " form-control"
            )

    def clean_email(self):
        """
        Валидация email на уникальность.

        Returns:
            str: Email, если валидация прошла

        Raises:
            forms.ValidationError: Если email уже существует
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("User with this email already exists."))
        return email


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя.

    Attributes:
        username: Email пользователя
        password: Пароль
    """

    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Enter your email")}
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Enter password")}
        ),
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением CSS классов.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                field.widget.attrs.get("class", "") + " form-control"
            )
