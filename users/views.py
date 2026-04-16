from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileEditForm


def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('core:home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form, 'active': 'register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # username — это email, который ввёл пользователь
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
                return redirect('core:home')
        messages.error(request, 'Неверный email или пароль')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form, 'active': 'login'})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('core:home')


@login_required
def profile_view(request):
    """Просмотр профиля пользователя"""
    return render(request, 'users/profile.html', {'active': 'profile'})


@login_required
def profile_edit_view(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=request.user.profile, user=request.user)

    return render(request, 'users/profile_edit.html', {'form': form, 'active': 'profile'})