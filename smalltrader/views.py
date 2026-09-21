import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import *
from .forms import AddGoodsForm, FeedbackForm


def index(request):

    goods_list = list(Good.objects.active().in_stock())
    random_goods = random.sample(goods_list, min(3, len(goods_list)))
    return render(request, 'smalltrader/index.html', {'goods': random_goods})

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

def edit_goods(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    
    if request.method == 'POST':
        form = AddGoodsForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            return redirect('good_detail', good_id=good.id)
    else:
        form = AddGoodsForm(instance=good)
    
    context = {
        'form': form,
        'good': good,
        'page_title': f'Редактирование: {good.title}',
    }
    return render(request, 'smalltrader/add_goods.html', context)

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(**form.cleaned_data)
            return redirect('home')