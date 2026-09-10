import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Good, Category, Rarity
from .forms import AddGoodsForm, FeedbackForm


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

def add_goods(request):
    if request.method == 'POST':
        form = AddGoodsForm(request.POST, request.FILES)
        if form.is_valid():
            good = form.save()
            return redirect('good_detail', good_id=good.id)
    else:
        form = AddGoodsForm()
    
    context = {
        'form': form,
        'page_title': 'Добавить товар',
    }
    return render(request, 'smalltrader/add_goods.html', context)


def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print('=' * 50)
            print('НОВОЕ СООБЩЕНИЕ ОБРАТНОЙ СВЯЗИ')
            print('=' * 50)
            print(f'Тема: {form.cleaned_data["subject"]}')
            print(f'Email: {form.cleaned_data["email"]}')
            print(f'Сообщение: {form.cleaned_data["text"]}')
            print('=' * 50)
            
            return redirect('home')
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'page_title': 'Обратная связь',
    }
    return render(request, 'smalltrader/contact.html', context)