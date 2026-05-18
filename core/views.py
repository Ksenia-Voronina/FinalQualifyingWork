from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from spaces.models import Space
from .forms import ContactForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import ContactMessage


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
    """Страница 'Контакты' с формой обратной связи"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем сообщение в базу данных
            contact = form.save()

            # Формируем письмо
            subject = f'Сообщение с сайта: {contact.subject}'
            message = f'От: {contact.name} ({contact.email})\n\n{contact.message}'

            # Отправляем письмо (синхронно)
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке. Пожалуйста, попробуйте позже.')
                print(f'Ошибка отправки письма: {e}')

            return redirect('core:contacts')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()

    return render(request, 'core/contacts.html', {
        'form': form,
        'active': 'contacts'
    })


@staff_member_required
def reply_to_user(request, id):
    """Перенаправляет администратора на Яндекс.Почту для ответа"""
    message = get_object_or_404(ContactMessage, id=id)
    return redirect(message.get_yandex_mail_link())


def faq_view(request):
    """Страница 'Часто задаваемые вопросы'"""
    return render(request, 'core/faq.html')