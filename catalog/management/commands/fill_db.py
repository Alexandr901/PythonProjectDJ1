from django.core.management import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        # Удаляем все продукты и категории
        from catalog.models import Product, Category

        with transaction.atomic():
            Product.objects.all().delete()
            Category.objects.all().delete()

            # Загружаем фикстуры
            call_command('loaddata', 'category_data.json', app_label='catalog')
            call_command('loaddata', 'product_data.json', app_label='catalog')

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены из фикстур'))
