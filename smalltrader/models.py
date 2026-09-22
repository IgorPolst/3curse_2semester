from django.contrib.auth.models import User 
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)
    color = models.CharField('Цвет для Bootstrap', max_length=50, default='secondary')
    icon = models.CharField('Иконка (Font Awesome)', max_length=50, blank=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name



class Rarity(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL-идентификатор', max_length=50, unique=True)
    color = models.CharField('Цвет для Bootstrap', max_length=50, default='secondary')
    value = models.PositiveSmallIntegerField('Значение редкости (1-6)', default=1, validators=[MinValueValidator(1), MaxValueValidator(6),])
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Редкость'
        verbose_name_plural = 'Редкости'
        ordering = ['value']
    
    def __str__(self):
        return self.name

class GoodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def in_stock(self):
        return self.filter(in_stock=True)

class Feedback(models.Model):
    subject = models.CharField('Тема', max_length=200)
    email = models.EmailField('Email')
    text = models.TextField('Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('URL-идентификатор', max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_goods', args=[self.slug])



class Good(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-идентификатор', max_length=200, unique=True)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='goods/', blank=True, null=True, default='goods/default.png')
    
    price = models.PositiveIntegerField('Цена (золотых)', default=0)
    in_stock = models.BooleanField('В наличии', default=True)
    quantity = models.PositiveIntegerField('Количество на складе', default=0)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goods',
        verbose_name='Категория'
    )
    rarity = models.ForeignKey(
        Rarity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goods',
        verbose_name='Редкость'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='goods',
        verbose_name='Теги',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goods',
        verbose_name='Продавец'
    )
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активно', default=True)

    objects = GoodQuerySet.as_manager()
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'in_stock']),
            models.Index(fields=['category']),
            models.Index(fields=['rarity']),
        ]
    
    def __str__(self):
        return f'{self.title} ({self.price} зол.)'

class Comment(models.Model):
    
    good = models.ForeignKey(
        Good,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Товар',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.author.username} → {self.good.title}'


