import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from smalltrader.models import Good


class Command(BaseCommand):
    help = 'Копирует все картинки из static/images/ в media/goods/ и привязывает к товарам'

    def handle(self, *args, **options):
        # Папки
        source_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        target_dir = os.path.join(settings.MEDIA_ROOT, 'goods')
        
        # Проверяем, что папка с исходниками существует
        if not os.path.exists(source_dir):
            self.stdout.write(self.style.ERROR(f'❌ Папка не найдена: {source_dir}'))
            return
        
        # Создаём папку назначения
        os.makedirs(target_dir, exist_ok=True)
        
        # Получаем список всех файлов в папке
        image_files = os.listdir(source_dir)
        
        if not image_files:
            self.stdout.write(self.style.WARNING('⚠️ В папке static/images/ нет картинок'))
            return
        
        self.stdout.write(f'📁 Найдено картинок: {len(image_files)}')
        
        # Копируем картинки
        for image_name in image_files:
            source_path = os.path.join(source_dir, image_name)
            target_path = os.path.join(target_dir, image_name)
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, target_path)
                self.stdout.write(self.style.SUCCESS(f'Скопирована: {image_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Все картинки скопированы в: {target_dir}'))
        
        # Привязываем картинки к товарам по имени файла
        self.stdout.write('\nПривязываем картинки к товарам...')
        
        for image_name in image_files:
            # Убираем расширение, получаем slug
            slug = os.path.splitext(image_name)[0]  # wheat.jpg -> wheat
            image_path = f'goods/{image_name}'
            
            try:
                good = Good.objects.get(slug=slug)
                good.image = image_path
                good.save()
                self.stdout.write(self.style.SUCCESS(f'{slug}: {image_path}'))
            except Good.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Товар с slug="{slug}" не найден'))
            except Good.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'Несколько товаров с slug="{slug}"'))
        
        self.stdout.write(self.style.SUCCESS('Готово!'))