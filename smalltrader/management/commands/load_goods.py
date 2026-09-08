from django.core.management.base import BaseCommand
from django.utils.text import slugify
from smalltrader.models import Good, Category, Rarity


class Command(BaseCommand):
    help = 'Загружает товары из списка в базу данных'

    def handle(self, *args, **options):
        # Данные товаров (с slug для каждого)
        goods_data = [
            # === ЕДА ===
            {
                'title': 'Пшеница',
                'slug': 'pshenica',
                'description': 'Широко распространённое злаковое растение, основа хлеба',
                'image': 'goods/wheat.jpg',
                'price': 50,
                'in_stock': True,
                'quantity': 100,
                'category_slug': 'food',
                'rarity_slug': 'common',
            },
            {
                'title': 'Мёд',
                'slug': 'med',
                'description': 'Натуральный продукт с пасек, ценится за сладость',
                'image': 'goods/honey.jpg',
                'price': 200,
                'in_stock': True,
                'quantity': 50,
                'category_slug': 'food',
                'rarity_slug': 'uncommon',
            },
            {
                'title': 'Соль',
                'slug': 'sol',
                'description': 'Белое золото средневековья, незаменимый консервант',
                'image': 'goods/salt.jpg',
                'price': 300,
                'in_stock': True,
                'quantity': 30,
                'category_slug': 'food',
                'rarity_slug': 'rare',
            },
            {
                'title': 'Чёрный перец',
                'slug': 'chernyy-perets',
                'description': 'Пряность из далёких стран, доступная лишь знати',
                'image': 'goods/pepper.jpg',
                'price': 500,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'food',
                'rarity_slug': 'epic',
            },
            {
                'title': 'Сушёная рыба',
                'slug': 'sushyonaya-ryba',
                'description': 'Проверенный запас для долгих путешествий',
                'image': 'goods/fish_dried.jpg',
                'price': 80,
                'in_stock': True,
                'quantity': 200,
                'category_slug': 'food',
                'rarity_slug': 'common',
            },
            
            # === ОРУЖИЕ ===
            {
                'title': 'Меч простой',
                'slug': 'mech-prostoy',
                'description': 'Стальной меч для ополченца, надёжен в бою',
                'image': 'goods/sword_simple.jpg',
                'price': 150,
                'in_stock': True,
                'quantity': 30,
                'category_slug': 'weapon',
                'rarity_slug': 'common',
            },
            {
                'title': 'Арбалет',
                'slug': 'arbalet',
                'description': 'Дальнобойное оружие, пробивает кольчугу',
                'image': 'goods/crossbow.jpg',
                'price': 350,
                'in_stock': True,
                'quantity': 20,
                'category_slug': 'weapon',
                'rarity_slug': 'uncommon',
            },
            {
                'title': 'Дамоклов меч',
                'slug': 'damoklov-mech',
                'description': 'Двуручный клинок с закалённой сталью',
                'image': 'goods/greatsword.jpg',
                'price': 600,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'weapon',
                'rarity_slug': 'rare',
            },
            {
                'title': 'Посох Архимага',
                'slug': 'posokh-arkhimaga',
                'description': 'Древняя реликвия с остатками магической силы',
                'image': 'goods/archmage_staff.jpg',
                'price': 1200,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'weapon',
                'rarity_slug': 'legendary',
            },
            {
                'title': 'Кинжал разведчика',
                'slug': 'kinzhal-razvedchika',
                'description': 'Короткий клинок с ядом на лезвии',
                'image': 'goods/dagger.jpg',
                'price': 250,
                'in_stock': True,
                'quantity': 15,
                'category_slug': 'weapon',
                'rarity_slug': 'uncommon',
            },
            
            # === БРОНЯ ===
            {
                'title': 'Кожаный доспех',
                'slug': 'kozhanyy-dospekh',
                'description': 'Доступная броня для разведчиков и лучников',
                'image': 'goods/leather_armor.jpg',
                'price': 200,
                'in_stock': True,
                'quantity': 25,
                'category_slug': 'armor',
                'rarity_slug': 'common',
            },
            {
                'title': 'Кольчуга',
                'slug': 'kolchuga',
                'description': 'Спасает от рубящих ударов, популярна у рыцарей',
                'image': 'goods/chainmail.jpg',
                'price': 450,
                'in_stock': True,
                'quantity': 10,
                'category_slug': 'armor',
                'rarity_slug': 'uncommon',
            },
            {
                'title': 'Доспех тамплиера',
                'slug': 'dospekh-tampliera',
                'description': 'Полный латный доспех, непробиваемый для стрел',
                'image': 'goods/knight_armor.jpg',
                'price': 800,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'armor',
                'rarity_slug': 'rare',
            },
            {
                'title': 'Щит Легионера',
                'slug': 'shchit-legionera',
                'description': 'Массивный скутум с металлической окантовкой',
                'image': 'goods/legion_shield.jpg',
                'price': 300,
                'in_stock': True,
                'quantity': 20,
                'category_slug': 'armor',
                'rarity_slug': 'uncommon',
            },
            {
                'title': 'Шлем драконоборца',
                'slug': 'shlem-drakonobortsa',
                'description': 'Легендарный шлем, выдержал дыхание дракона',
                'image': 'goods/dragon_helmet.jpg',
                'price': 1500,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'armor',
                'rarity_slug': 'legendary',
            },
            
            # === ТРАНСПОРТ ===
            {
                'title': 'Вьючная лошадь',
                'slug': 'vyuchnaya-loshad',
                'description': 'Выносливое животное для перевозки грузов',
                'image': 'goods/pack_horse.jpg',
                'price': 120,
                'in_stock': True,
                'quantity': 8,
                'category_slug': 'transport',
                'rarity_slug': 'common',
            },
            {
                'title': 'Боевой конь',
                'slug': 'boevoy-kon',
                'description': 'Обучен для боя, не боится звуков битвы',
                'image': 'goods/war_horse.jpg',
                'price': 400,
                'in_stock': True,
                'quantity': 5,
                'category_slug': 'transport',
                'rarity_slug': 'uncommon',
            },
            {
                'title': 'Купеческая карета',
                'slug': 'kupecheskaya-kareta',
                'description': 'Позволяет перевозить товары в безопасности',
                'image': 'goods/merchant_carriage.jpg',
                'price': 600,
                'in_stock': True,
                'quantity': 3,
                'category_slug': 'transport',
                'rarity_slug': 'rare',
            },
            {
                'title': 'Боевая колесница',
                'slug': 'boevaya-kolesnitsa',
                'description': 'Скоростная платформа для лучников в бою',
                'image': 'goods/war_chariot.jpg',
                'price': 900,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'transport',
                'rarity_slug': 'epic',
            },
            {
                'title': 'Дракон (яйцо)',
                'slug': 'drakon-yaytso',
                'description': 'Экзотический транспорт будущего, если вырастет',
                'image': 'goods/dragon_egg.jpg',
                'price': 5000,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'transport',
                'rarity_slug': 'mythic',
            },
            
            # === ИНСТРУМЕНТЫ ===
            {
                'title': 'Кузнечный молот',
                'slug': 'kuznechnyy-molot',
                'description': 'Основной инструмент кузнеца для ковки стали',
                'image': 'goods/blacksmith_hammer.jpg',
                'price': 80,
                'in_stock': True,
                'quantity': 50,
                'category_slug': 'tools',
                'rarity_slug': 'common',
            },
            {
                'title': 'Плотницкий топор',
                'slug': 'plotnitskiy-topor',
                'description': 'Инструмент плотника для строительства и обороны',
                'image': 'goods/carpenter_axe.jpg',
                'price': 100,
                'in_stock': True,
                'quantity': 40,
                'category_slug': 'tools',
                'rarity_slug': 'common',
            },
            {
                'title': 'Астролябия',
                'slug': 'astrolyabiya',
                'description': 'Навигационный прибор для путешествий по морю',
                'image': 'goods/astrolabe.jpg',
                'price': 350,
                'in_stock': True,
                'quantity': 5,
                'category_slug': 'tools',
                'rarity_slug': 'rare',
            },
            {
                'title': 'Алхимический набор',
                'slug': 'alkhimicheskiy-nabor',
                'description': 'Позволяет создавать зелья и лекарства',
                'image': 'goods/alchemy_set.jpg',
                'price': 500,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'tools',
                'rarity_slug': 'epic',
            },
            {
                'title': 'Гномий компас',
                'slug': 'gnomiy-kompas',
                'description': 'Зачарованный компас, укажет путь в любых землях',
                'image': 'goods/gnome_compass.jpg',
                'price': 750,
                'in_stock': False,
                'quantity': 0,
                'category_slug': 'tools',
                'rarity_slug': 'legendary',
            },
        ]

        # Загружаем товары
        for good_data in goods_data:
            try:
                # Извлекаем category_slug и rarity_slug
                category_slug = good_data.pop('category_slug')
                rarity_slug = good_data.pop('rarity_slug')
                
                # Получаем объекты категории и редкости
                category = Category.objects.get(slug=category_slug)
                rarity = Rarity.objects.get(slug=rarity_slug)
                
                # Создаём или обновляем товар
                good, created = Good.objects.get_or_create(
                    slug=good_data['slug'],
                    defaults={
                        **good_data,
                        'category': category,
                        'rarity': rarity,
                    }
                )
        
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлен товар: {good.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Товар уже существует: {good.title}'))
                    
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория не найдена: {category_slug}'))
            except Rarity.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Редкость не найдена: {rarity_slug}'))
            except KeyError as e:
                self.stdout.write(self.style.ERROR(f'Отсутствует ключ: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))