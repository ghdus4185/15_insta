from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)


def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user
    if you == me:
        return redirect('account:user_page', id)
    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followers.add(me)
    return redirect('accounts:user_page', id)


def delete(request, id):
    user_info = get_object_or_404(User, id=id)
    user = request.user
    if user_info == user:
        if request.method == "POST":
            user.delete()
    return redirect('posts:index')


def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def profile(request):
    user_info = request.user
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)
