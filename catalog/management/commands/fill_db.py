import os

from django.conf import settings
from django.core.files import File
from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Fill database with test data"

    def handle(self, *args, **options):
        # Удаляем все продукты
        Product.objects.all().delete()
        # Удаляем все категории
        Category.objects.all().delete()

        # Создаем категории
        category_list = [
            {"name": "Электроника", "description": "Гаджеты и устройства"},
            {"name": "Одежда", "description": "Модная одежда"},
            {"name": "Книги", "description": "Литература разных жанров"},
        ]

        categories = []
        for category_item in category_list:
            category = Category.objects.create(**category_item)
            categories.append(category)
            self.stdout.write(f"Создана категория: {category.name}")

        # Создаем продукты
        product_list = [
            {
                "name": "Ноутбук",
                "description": "Мощный игровой ноутбук с процессором Intel Core i7 и видеокартой NVIDIA GeForce RTX 3060. Идеально подходит для работы и игр.",
                "category": categories[0],
                "price": 1000,
            },
            {
                "name": "Смартфон",
                "description": "Современный смартфон с большим экраном, мощным процессором и отличной камерой. Работает на операционной системе Android.",
                "category": categories[0],
                "price": 800,
            },
            {
                "name": "Футболка",
                "description": "Хлопковая футболка премиум-качества. Доступна в различных цветах и размерах. Удобная и стильная.",
                "category": categories[1],
                "price": 20,
            },
            {
                "name": "Роман",
                "description": "Захватывающий роман от известного автора. Интригующий сюжет и глубокие персонажи не оставят вас равнодушными.",
                "category": categories[2],
                "price": 15,
            },
        ]

        for product_item in product_list:
            product = Product.objects.create(**product_item)
            self.stdout.write(f"Создан продукт: {product.name}")

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))
