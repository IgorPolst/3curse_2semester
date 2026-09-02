import random
from django.shortcuts import render
from django.db.models import Q
from .models import Good, Category, Rarity


def index(request):

    goods = Good.objects.filter(in_stock=True, is_active=True)

    if goods.count() > 3:
        random_goods = random.sample(list(goods), 3)
    else:
        random_goods = goods

    context = {
        'goods': random_goods,
        'page_title': 'Главная страница',
    }
    return render(request, 'smalltrader/index.html', context)

def market(request):
        
        goods = Good.objects.filter(is_active=True).select_related('category', 'rarity')
        categories = {cat.slug: cat for cat in Category.objects.all()}
        rarity_levels = {rarity.slug: rarity for rarity in Rarity.objects.all()}

        context = {
            'categories': categories,
            'rarity_levels': rarity_levels,
            'goods': goods,
            'page_title': 'Торговая площадь',
        }

        return render(request, 'smalltrader/market.html', context)