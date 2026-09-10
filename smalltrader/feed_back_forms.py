from django import forms

class FeedbackForm(forms.Form):
    
    subject = forms.CharField(
        label='Тема письма',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите тему письма'
        })
    )
    email = forms.EmailField(
        label='Email отправителя',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )
    text = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите ваше сообщение...'
        })
    )