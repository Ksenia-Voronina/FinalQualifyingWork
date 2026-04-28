from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .models import Space
from bookings.models import Booking


class SpaceListView(ListView):
    """Список всех пространств"""
    model = Space
    template_name = 'spaces/space_list.html'
    context_object_name = 'spaces'
    paginate_by = 12

    def get_queryset(self):
        """Только доступные для бронирования пространства"""
        return Space.objects.filter(is_available=True)


class SpaceDetailView(DetailView):
    """Детальная страница пространства"""
    model = Space
    template_name = 'spaces/space_detail.html'
    context_object_name = 'space'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        space = self.get_object()

        # Время работы пространства
        WORK_START = 8  # 8:00
        WORK_END = 20  # 20:00

        # Получаем подтверждённые бронирования (pending и confirmed)
        bookings = Booking.objects.filter(
            space=space,
            status__in=['pending', 'confirmed'],
            end_datetime__gte=timezone.now()
        )

        booked_dates_full = []  # полностью занятые дни
        booked_dates_partial = []  # частично занятые дни
        booked_hours = {}  # словарь: дата -> список занятых часов

        now = timezone.now()

        for booking in bookings:
            start = booking.start_datetime
            end = booking.end_datetime

            # Перебираем каждый день в диапазоне бронирования
            current_date = start.date()
            end_date = end.date()

            while current_date <= end_date:
                date_str = current_date.isoformat()

                # Определяем часы бронирования для этого дня с учётом часового пояса
                hours = []

                # Начало дня: максимум между началом бронирования и 8:00
                day_start_dt = timezone.make_aware(
                    datetime(current_date.year, current_date.month, current_date.day, WORK_START, 0)
                )
                # Конец дня: минимум между концом бронирования и 20:00
                day_end_dt = timezone.make_aware(
                    datetime(current_date.year, current_date.month, current_date.day, WORK_END, 0)
                )

                # Бронирование может начинаться позже 8:00
                actual_start = max(start, day_start_dt) if start > day_start_dt else day_start_dt
                # Бронирование может заканчиваться раньше 20:00
                actual_end = min(end, day_end_dt) if end < day_end_dt else day_end_dt

                # Если бронирование пересекается с рабочим временем
                if actual_start < actual_end:
                    for hour in range(actual_start.hour, actual_end.hour):
                        hours.append(hour)

                if hours:
                    # Добавляем занятые часы в словарь
                    if date_str not in booked_hours:
                        booked_hours[date_str] = []
                    booked_hours[date_str].extend(hours)
                    # Убираем дубликаты и сортируем
                    booked_hours[date_str] = sorted(list(set(booked_hours[date_str])))

                    # Определяем статус дня
                    # Полный рабочий день: 8:00-20:00 = 12 часов
                    if len(booked_hours[date_str]) >= 12:
                        if date_str not in booked_dates_full:
                            booked_dates_full.append(date_str)
                    else:
                        if date_str not in booked_dates_partial:
                            booked_dates_partial.append(date_str)

                current_date += timedelta(days=1)

        context['booked_dates_full'] = json.dumps(booked_dates_full)
        context['booked_dates_partial'] = json.dumps(booked_dates_partial)
        context['booked_hours'] = json.dumps(booked_hours)

        return context