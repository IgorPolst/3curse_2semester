from django.contrib import admin
from .models import Category, Rarity, Good, Tag, Comment


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

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'good', 'text_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'good__title']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    text_preview.short_description = 'Текст'


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