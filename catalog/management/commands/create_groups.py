from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    """
    Кастомная команда для создания групп и назначения разрешений.

    Создает группу "Модератор продуктов" и назначает необходимые разрешения.
    """

    help = 'Создает группы и назначает разрешения для модераторов'

    def handle(self, *args, **options):
        """
        Основной метод выполнения команды.

        Args:
            *args: Аргументы команды
            **options: Опции команды
        """
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        # Получаем разрешения
        content_type = ContentType.objects.get_for_model(Product)

        # Кастомное разрешение на отмену публикации
        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # Разрешение на удаление продукта
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Разрешение на изменение продукта
        change_permission = Permission.objects.get(
            codename='change_product',
            content_type=content_type
        )

        # Назначаем разрешения группе
        moderator_group.permissions.add(
            unpublish_permission,
            delete_permission,
            change_permission
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Разрешения назначены группе "Модератор продуктов":\n'
                '- Может отменять публикацию продукта\n'
                '- Может удалять любой продукт\n'
                '- Может изменять любой продукт'
            )
        )

