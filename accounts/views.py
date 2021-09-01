from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import *

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User(username=cd['username'], email=cd['email'], first_name=cd['first_name'], last_name=cd['last_name'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_success.html', {'new_user': new_user})
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(username=cd['username'])
            auth.login(request, user)
            return render(request, 'accounts/login_success.html')
        return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return render(request, 'accounts/logout.html')
