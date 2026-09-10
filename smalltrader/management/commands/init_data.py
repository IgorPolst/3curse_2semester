from django.core.management.base import BaseCommand
from smalltrader.models import Category, Rarity


class Command(BaseCommand):
    help = 'Инициализирует начальные данные (категории и редкости)'

    def handle(self, *args, **options):
        # Создаём категории
        categories = [
            {'name': 'Еда', 'slug': 'food', 'color': 'success', 'icon': 'fa-utensils'},
            {'name': 'Оружие', 'slug': 'weapon', 'color': 'danger', 'icon': 'fa-sword'},
            {'name': 'Броня', 'slug': 'armor', 'color': 'primary', 'icon': 'fa-shield-halved'},
            {'name': 'Транспорт', 'slug': 'transport', 'color': 'warning', 'icon': 'fa-horse'},
            {'name': 'Инструменты', 'slug': 'tools', 'color': 'secondary', 'icon': 'fa-hammer'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {category.name}'))

        # Создаём редкости
        rarities = [
            {'name': 'Обычный', 'slug': 'common', 'color': 'secondary', 'value': 1},
            {'name': 'Необычный', 'slug': 'uncommon', 'color': 'success', 'value': 2},
            {'name': 'Редкий', 'slug': 'rare', 'color': 'primary', 'value': 3},
            {'name': 'Эпический', 'slug': 'epic', 'color': 'purple', 'value': 4},
            {'name': 'Легендарный', 'slug': 'legendary', 'color': 'warning', 'value': 5},
            {'name': 'Мифический', 'slug': 'mythic', 'color': 'danger', 'value': 6},
        ]

        for rarity_data in rarities:
            rarity, created = Rarity.objects.get_or_create(
                slug=rarity_data['slug'],
                defaults=rarity_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана редкость: {rarity.name}'))

        self.stdout.write(self.style.SUCCESS('✅ Начальные данные загружены!'))