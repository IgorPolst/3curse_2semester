import random
from django.shortcuts import render
from .goods_data import get_all_goods


def index(request):

    all_goods = get_all_goods()


    shuffled = random.sample(all_goods, min(3, len(all_goods)))
    
    context = {
        'goods': shuffled,
        'page_title': 'Главная страница',
    }
    return render(request, 'smalltrader/index.html', context)

def market(request):
    # Категории товаров
        categories = {
            'food': {'name': 'Еда', 'color': 'success'},
            'weapon': {'name': 'Оружие', 'color': 'danger'},
            'armor': {'name': 'Броня', 'color': 'primary'},
            'transport': {'name': 'Транспорт', 'color': 'warning'},
            'tools': {'name': 'Инструменты', 'color': 'secondary'},
        }
        
        # Редкость товаров
        rarity_levels = {
            'common': {'name': 'Обыч.', 'color': 'secondary', 'value': 1},
            'uncommon': {'name': 'Необыч.', 'color': 'success', 'value': 2},
            'rare': {'name': 'Ред.', 'color': 'primary', 'value': 3},
            'epic': {'name': 'Эпич.', 'color': 'purple', 'value': 4},
            'legendary': {'name': 'Леген.', 'color': 'warning', 'value': 5},
            'mythic': {'name': 'Миф.', 'color': 'danger', 'value': 6},
        }
        
        goods = get_all_goods()

        context = {
            'categories': categories,
            'rarity_levels': rarity_levels,
            'goods': goods,
            'page_title': 'Торговая площадь',
        }

        return render(request, 'smalltrader/market.html', context)