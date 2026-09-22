import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Good, Category, Rarity, Feedback, Tag
from .forms import AddGoodsForm, FeedbackForm, CustomUserCreationForm, CommentForm
from django.contrib.auth.decorators import login_required      
from django.contrib.auth.forms import UserCreationForm          
from django.contrib.auth import login 
from django.contrib import messages
from django.views.decorators.http import require_POST



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
        "comment_form": CommentForm(), 
        "page_title": good.title,
    }
    return render(request, "smalltrader/good_detail.html", context)

@login_required 
def add_goods(request):
    if request.method == 'POST':
        form = AddGoodsForm(request.POST, request.FILES)
        if form.is_valid():
            good = form.save(commit=False)
            good.author = request.user
            good.save()
            form.save_m2m()
            messages.success(request, f'Товар «{good.title}» успешно создан!')
            return redirect('good_detail', good_id=good.id)
        else:
            messages.error(request, 'Ошибка при создании товара. Проверьте поля.')
    else:
        form = AddGoodsForm()

    context = {
        'form': form,
        'page_title': 'Добавить товар',
        'form_title': 'Добавить товар',
        'submit_label': 'Создать товар',
        'cancel_url': 'market',
    }
    return render(request, 'smalltrader/add_goods.html', context)

@login_required
def edit_goods(request, good_id):
    good = get_object_or_404(Good, id=good_id)

    can_edit = (
        good.author == request.user
        or request.user.is_superuser
    )

    if not can_edit:
        messages.error(request, 'У вас нет прав на редактирование этого товара.')
        return redirect('good_detail', good_id=good.id)
    
    if request.method == 'POST':
        form = AddGoodsForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            messages.success(request, f'Товар «{good.title}» обновлён!')
            return redirect('good_detail', good_id=good.id)
        else:
            messages.error(request, 'Ошибка при сохранении.')
    else:
        form = AddGoodsForm(instance=good)

    context = {
        'form': form,
        'good': good,
        'page_title': f'Редактирование: {good.title}',
        'form_title': f'Редактирование: {good.title}',
        'submit_label': 'Сохранить изменения',
        'cancel_url': 'good_detail',
        'cancel_url_arg': good.id,
    }
    return render(request, 'smalltrader/add_goods.html', context)

def tag_goods(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    goods = Good.objects.filter(tags=tag, is_active=True).select_related('category', 'rarity')
    
    context = {
        'tag': tag,
        'goods': goods,
        'page_title': f'Тег: {tag.name}',
        'categories': {cat.slug: cat for cat in Category.objects.all()},
        'rarity_levels': {rarity.slug: rarity for rarity in Rarity.objects.all()},
    }
    return render(request, 'smalltrader/market.html', context)    

def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
        
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(**form.cleaned_data)
            messages.success(request, 'Сообщение отправлено! Мы свяжемся с вами.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка: проверьте форму.')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'page_title': 'Обратная связь',
    }
    return render(request, 'smalltrader/contact.html', context)

@login_required
@require_POST
def add_comment(request, good_id):

    good = get_object_or_404(Good, id=good_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.good = good
        comment.author = request.user
        comment.save()
        messages.success(request, 'Комментарий добавлен!')
    else:
        messages.error(request, 'Ошибка: комментарий не может быть пустым.')
    
    return redirect('good_detail', good_id=good.id)