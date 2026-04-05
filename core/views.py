from django.shortcuts import render


def home_view(request):
    """Отображает главную страницу сайта"""
    return render(request, 'core/base.html')