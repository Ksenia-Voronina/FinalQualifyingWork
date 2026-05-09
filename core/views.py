from django.shortcuts import render
from spaces.models import Space


def home_view(request):
    """Отображает главную страницу"""
    featured_spaces = Space.objects.filter(
        show_on_homepage=True,
        is_available=True
    )[:3]  # максимум 3 пространства на главной

    context = {
        'active': 'home',  # для подсветки активного пункта меню
        'featured_spaces': featured_spaces,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """Страница 'О проекте'"""
    return render(request, 'core/about.html')


def contacts_view(request):
    """Страница 'Контакты'"""
    return render(request, 'core/contacts.html')


def faq_view(request):
    """Страница 'Часто задаваемые вопросы'"""
    return render(request, 'core/faq.html')