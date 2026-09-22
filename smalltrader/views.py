import random
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Good, Category, Rarity, Feedback, Tag
from .forms import AddGoodsForm, FeedbackForm, CustomUserCreationForm, CommentForm
from django.contrib.auth.decorators import login_required               
from django.contrib.auth import login 
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse



def index(request):

    goods_list = list(Good.objects.active().in_stock())
    random_goods = random.sample(goods_list, min(3, len(goods_list)))
    return render(request, 'smalltrader/index.html', {'goods': random_goods})

class MarketView(ListView):
    model = Good
    template_name = 'smalltrader/market.html'
    context_object_name = 'goods'
    
    def get_queryset(self):
        return Good.objects.filter(is_active=True).select_related('category', 'rarity')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = {cat.slug: cat for cat in Category.objects.all()}
        context['rarity_levels'] = {rarity.slug: rarity for rarity in Rarity.objects.all()}
        context['page_title'] = 'Торговая площадь'
        return context


class GoodDetailView(DetailView):
    model = Good
    template_name = 'smalltrader/good_detail.html'
    context_object_name = 'good'
    pk_url_kwarg = 'good_id'
    
    def get_queryset(self):
        return Good.objects.select_related('category', 'rarity').prefetch_related('comments__author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good = self.object
        
        context['related_goods'] = Good.objects.filter(
            category=good.category,
            is_active=True
        ).exclude(id=good.id)[:4]
        context['comment_form'] = CommentForm()
        context['page_title'] = good.title
        return context


class AddGoodsView(LoginRequiredMixin, CreateView):
    model = Good
    form_class = AddGoodsForm
    template_name = 'smalltrader/add_goods.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить товар'
        context['form_title'] = 'Добавить товар'
        context['submit_label'] = 'Создать товар'
        context['cancel_url'] = 'market'
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Товар «{form.instance.title}» успешно создан!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('good_detail', kwargs={'good_id': self.object.id})


class EditGoodsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Good
    form_class = AddGoodsForm
    template_name = 'smalltrader/add_goods.html'
    pk_url_kwarg = 'good_id'
    raise_exception = False
    
    def test_func(self):
        good = self.get_object()
        return (
            good.author == self.request.user
            or self.request.user.is_superuser
            or good.author is None
        )
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на редактирование.')
        return redirect('good_detail', good_id=self.get_object().id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good = self.object
        context['good'] = good
        context['page_title'] = f'Редактирование: {good.title}'
        context['form_title'] = f'Редактирование: {good.title}'
        context['submit_label'] = 'Сохранить изменения'
        context['cancel_url'] = 'good_detail'
        context['cancel_url_arg'] = good.id
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Товар «{form.instance.title}» обновлён!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('good_detail', kwargs={'good_id': self.object.id})

class DeleteGoodsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Good
    template_name = 'smalltrader/good_confirm_delete.html'
    context_object_name = 'good'
    pk_url_kwarg = 'good_id'
    success_url = reverse_lazy('market')
    
    def test_func(self):
        good = self.get_object()
        return (
            good.author == self.request.user
            or self.request.user.is_superuser
        )
    
    def form_valid(self, form):
        messages.success(self.request, f'Товар «{self.object.title}» удалён.')
        return super().form_valid(form)

class TagGoodsView(ListView):
    model = Good
    template_name = 'smalltrader/market.html'
    context_object_name = 'goods'
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Good.objects.filter(
            tags=self.tag,
            is_active=True
        ).select_related('category', 'rarity')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['categories'] = {cat.slug: cat for cat in Category.objects.all()}
        context['rarity_levels'] = {rarity.slug: rarity for rarity in Rarity.objects.all()}
        context['page_title'] = f'Тег: {self.tag.name}'
        return context  

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
    
    return redirect('good_detail', good_id=good.id)