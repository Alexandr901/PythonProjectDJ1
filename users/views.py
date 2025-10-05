from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserLoginForm, UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    """
    Представление для регистрации пользователя.

    Attributes:
        model: Модель пользователя
        form_class: Форма регистрации
        template_name: Шаблон регистрации
        success_url: URL перенаправления после успешной регистрации
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """
        Обработка валидной формы с отправкой приветственного письма.

        Args:
            form: Валидная форма регистрации

        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        response = super().form_valid(form)

        # Автоматический вход после регистрации
        login(self.request, self.object)

        # Отправка приветственного письма
        self.send_welcome_email()

        return response

    def send_welcome_email(self):
        """
        Отправка приветственного письма новому пользователю.
        """
        subject = "Добро пожаловать в наш каталог!"
        message = f"""
        Уважаемый {self.object.get_full_name()},

        Благодарим вас за регистрацию в нашем каталоге товаров.

        Теперь вы можете:
        - Просматривать детальную информацию о товарах
        - Создавать и редактировать свои товары
        - Управлять своим профилем

        Если у вас возникли вопросы, свяжитесь с нашей службой поддержки.

        С уважением,
        Команда каталога товаров
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.object.email],
            fail_silently=False,
        )


class UserLoginView(LoginView):
    """
    Представление для авторизации пользователя.

    Attributes:
        form_class: Форма авторизации
        template_name: Шаблон авторизации
        redirect_authenticated_user: Перенаправление аутентифицированных пользователей
    """

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True
