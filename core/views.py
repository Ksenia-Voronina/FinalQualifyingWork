from django.shortcuts import render

def home_view(request):
    """Отображает главную страницу"""
    context = {
        'active': 'home',  # для подсветки активного пункта меню
    }
    return render(request, 'core/home.html', context)