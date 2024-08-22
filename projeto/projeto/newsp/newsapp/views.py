from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from PIL import Image 
import os
from django.conf import settings
from datetime import date 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from .models import News, Comment, Category
from django.contrib import messages

from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetView
)
from django.contrib.auth.decorators import login_required
from django.views import View

# Create your views here.

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('ja existe um usuario com esse username')

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return redirect('login')

        

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

    user = authenticate(username=username, password=senha)

    if user:
        login_django(request, user)

        return redirect('perfil')
    else:
        return HttpResponse('autenticação falhou. login ou senha inválidos.')

def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse('Plataforma')
    return HttpResponse('voce precisa estar logado')

def home(request):
    first_news = News.objects.first()
    three_news = News.objects.all()[1:4]
    three_categories = Category.objects.all()[0:3]

    return render(request, 'home.html',{
        'first_news':first_news,
        'three_news':three_news,
        'three_categories':three_categories

    })

def all_news(request):
    all_news=News.objects.all()
    return render(request, 'all-news.html',{
        'all_news':all_news
    })

# Deatil Page
def detail(request,id):
    news=News.objects.get(pk=id)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        comment=request.POST['message'] 
        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment
        )
        messages.success(request,'comment submitted but in moderation mode.')
    category=Category.objects.get(id=news.category.id)
    rel_news=News.objects.filter(category=category).exclude(id=id)
    comments=Comment.objects.filter(news=news,status=True).order_by('-id')
    return render(request, 'detail.html',{
        'news':news,
        'related_news':rel_news,
        'comments':comments
    })

def all_category(request):
    cats=Category.objects.all()
    return render(request,'category.html',{
        'cats':cats
    })

#fetch news in category
def category(request,id):
    category=Category.objects.get(id=id)
    news=News.objects.filter(category=category)
    return render(request,'category-news.html',{
        'all_news':news,
        'category':category
    })

def save(self, *args, **kwargs):
    # save the profile first
    super().save(*args, **kwargs)

    # resize the image
    img = Image.open(self.avatar.path)
    if img.height > 150 or img.width > 150:
        output_size = (150, 150)
        # create a thumbnail
        img.thumbnail(output_size)
        
        # overwrite the large image
        img.save(self.avatar.path)

from django.views import View

# ...

class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self,request):
        user_form = UserUpdateForm(
            request.POST, 
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request,'Your profile has been updated successfully')
            
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating you profile')
            
            return render(request, 'users/profile.html', context)