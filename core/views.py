from django.shortcuts import render

def home_view(request):
    """Отображает главную страницу"""
    context = {
        'active': 'home',  # для подсветки активного пункта меню
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