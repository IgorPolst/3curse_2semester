"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from smalltrader import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from smalltrader.forms import CustomAuthenticationForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('market/', views.market, name='market'),
    path('good/<int:good_id>/', views.good_detail, name='good_detail'),
    path('add/', views.add_goods, name='add_goods'),
    path('contact/', views.contact, name='contact'),  
    path('good/<int:good_id>/edit/', views.edit_goods, name='edit_goods'),     
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', 
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=CustomAuthenticationForm
         ), 
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('tag/<slug:slug>/', views.tag_goods, name='tag_goods'),
    path('good/<int:good_id>/comment/', views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
