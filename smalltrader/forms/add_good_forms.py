from django import forms
from django.utils.text import slugify
from ..models import Good


class AddGoodsForm(forms.ModelForm):
    class Meta:
        model = Good

        fields = [
            'title',
            'slug',
            'description',
            'image',
            'price',
            'in_stock',
            'quantity',
            'category',
            'rarity',
            'is_active',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'rarity': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'title': 'Название',
            'slug': 'URL-идентификатор',
            'description': 'Описание',
            'image': 'Изображение',
            'price': 'Цена (золотых)',
            'in_stock': 'В наличии',
            'quantity': 'Количество на складе',
            'category': 'Категория',
            'rarity': 'Редкость',
            'is_active': 'Активно',
        }

        help_texts = {
            'slug': 'Только латиница, цифры, дефис и подчеркивание.',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

