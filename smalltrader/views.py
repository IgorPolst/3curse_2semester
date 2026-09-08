import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
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

def good_detail(request: HttpRequest, good_id: int) -> HttpResponse:
    good = get_object_or_404(Good.objects.select_related('category', 'rarity'), id=good_id)
    
    related_goods = Good.objects.filter(
        category=good.category,
        is_active=True
    ).exclude(id=good.id)[:4]
    
    context = {
        "good": good,
        "related_goods": related_goods,
        "page_title": good.title,
    }
    return render(request, "smalltrader/good_detail.html", context)