from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Категория товара"""
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
    """Редкость товара"""
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL-идентификатор', max_length=50, unique=True)
    color = models.CharField('Цвет для Bootstrap', max_length=50, default='secondary')
    value = models.PositiveSmallIntegerField('Значение редкости (1-6)', default=1)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Редкость'
        verbose_name_plural = 'Редкости'
        ordering = ['value']
    
    def __str__(self):
        return self.name


class Good(models.Model):
    """Товар"""
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-идентификатор', max_length=200, unique=True)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='goods/', blank=True, null=True)
    
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
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} ({self.price} зол.)'
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('goods_detail', args=[self.slug])