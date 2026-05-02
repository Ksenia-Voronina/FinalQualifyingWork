from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from .models import Booking
from .forms import BookingForm
from spaces.models import Space

@login_required   # Проверка авторизован ли пользователь
def booking_create(request, space_id):
    space = get_object_or_404(Space, id=space_id, is_available=True)
    booked_slots = []
    selected_date = request.GET.get('date')

    # Формируем занятые слоты для выбранной даты (для отображения в шаблоне)
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            bookings_on_date = Booking.objects.filter(
                space=space,
                status__in=['pending', 'confirmed'],
                start_datetime__date=selected_date_obj
            )
            for booking in bookings_on_date:
                booked_slots.append({
                    'start': booking.start_datetime.strftime('%H:%M'),
                    'end': booking.end_datetime.strftime('%H:%M')
                })
        except ValueError:
            pass

    if request.method == 'POST':
        form = BookingForm(request.POST, space=space)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space
            booking.save()
            messages.success(request, f'Пространство "{space.name}" успешно забронировано!')
            return redirect('bookings:my_bookings')
    else:
        form = BookingForm()
        # Предзаполнение даты из параметра
        selected_date = request.GET.get('date')
        if selected_date:
            try:
                date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
                form = BookingForm(initial={'start_datetime': date_obj})
            except ValueError:
                pass

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'space': space,
        'selected_date': selected_date,
        'booked_slots': booked_slots,
    })


@login_required
def booking_list(request):
    """Список бронирований текущего пользователя"""
    bookings = Booking.objects.filter(user=request.user).select_related('space')

    # Разделяем на предстоящие и прошедшие
    upcoming = bookings.filter(end_datetime__gte=timezone.now()).order_by('start_datetime')
    past = bookings.filter(end_datetime__lt=timezone.now()).order_by('-start_datetime')

    return render(request, 'bookings/booking_list.html', {
        'upcoming': upcoming,
        'past': past,
        'active': 'bookings'
    })


@login_required
def booking_detail(request, id):
    """Детальная страница бронирования"""
    booking = get_object_or_404(Booking, id=id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'active': 'bookings'
    })


@login_required
def booking_cancel(request, id):
    """Отмена бронирования"""
    booking = get_object_or_404(Booking, id=id, user=request.user)

    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Бронирование "{booking.event_name}" отменено')

    return redirect('bookings:detail', id=booking.id)


def get_booked_slots(request, space_id):
    """Возвращает занятые слоты для выбранной даты (AJAX)"""
    space = get_object_or_404(Space, id=space_id)
    date_str = request.GET.get('date')

    if not date_str:
        return JsonResponse({'error': 'Дата не указана'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Неверный формат даты'}, status=400)

    # Получаем занятые бронирования
    bookings = Booking.objects.filter(
        space=space,
        status__in=['pending', 'confirmed'],
        start_datetime__date=selected_date
    )

    booked_slots = []
    for booking in bookings:
        booked_slots.append({
            'start': booking.start_datetime.strftime('%H:%M'),
            'end': booking.end_datetime.strftime('%H:%M')
        })

    return JsonResponse({
        'date': date_str,
        'booked_slots': booked_slots,
        'has_bookings': len(booked_slots) > 0
    })