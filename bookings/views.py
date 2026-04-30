from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Booking
from .forms import BookingForm
from spaces.models import Space


@login_required   # Проверка авторизован ли пользователь
def booking_create(request, space_id):
    space = get_object_or_404(Space, id=space_id, is_available=True)

    # Получаем дату из GET-параметра
    selected_date = request.GET.get('date')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space
            booking.save()
            messages.success(request, f'Пространство "{space.name}" успешно забронировано!')
            return redirect('bookings:my_bookings')
    else:
        form = BookingForm()

        # Если дата передана, подставляем её в форму
        if selected_date:
            try:
                date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
                initial_data = {
                    'start_datetime': date_obj,
                }
                form = BookingForm(initial=initial_data)
            except ValueError:
                pass

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'space': space,
        'selected_date': selected_date,  # передаём дату в шаблон
    })


@login_required
def booking_list(request):
    """Список бронирований текущего пользователя"""
    bookings = Booking.objects.filter(user=request.user).select_related('space')

    # Разделяем на предстоящие и прошедшие
    from django.utils import timezone
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