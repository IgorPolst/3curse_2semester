from django.contrib import admin
from .models import Category, Rarity, Good


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'value']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'in_stock', 'category', 'rarity', 'is_active']
    list_filter = ['category', 'rarity', 'in_stock', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'in_stock', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Характеристики', {
            'fields': ('price', 'in_stock', 'quantity')
        }),
        ('Категории', {
            'fields': ('category', 'rarity')
        }),
        ('Статус', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )