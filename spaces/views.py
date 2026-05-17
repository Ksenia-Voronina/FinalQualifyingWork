from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict
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

        # Получаем подтверждённые бронирования
        bookings = Booking.objects.filter(
            space=space,
            status__in=['pending', 'confirmed'],
            end_datetime__gte=timezone.now()
        )

        # Словарь для хранения суммарной длительности бронирований по дням (в часах)
        daily_total = defaultdict(float)
        booked_hours = {}  # словарь: дата -> список занятых часов (для JS, если нужно)

        for booking in bookings:
            start = booking.start_datetime
            end = booking.end_datetime

            current_date = start.date()
            end_date = end.date()

            while current_date <= end_date:
                date_str = current_date.isoformat()
                hours = []

                # Начало и конец рабочего дня для этой даты
                day_start_dt = timezone.make_aware(
                    datetime(current_date.year, current_date.month, current_date.day, WORK_START, 0)
                )
                day_end_dt = timezone.make_aware(
                    datetime(current_date.year, current_date.month, current_date.day, WORK_END, 0)
                )

                actual_start = max(start, day_start_dt) if start > day_start_dt else day_start_dt
                actual_end = min(end, day_end_dt) if end < day_end_dt else day_end_dt

                if actual_start < actual_end:
                    # Добавляем часы для booked_hours (для совместимости с JS)
                    for hour in range(actual_start.hour, actual_end.hour):
                        hours.append(hour)

                    # Рассчитываем длительность в часах для суммарного подсчёта
                    duration = (actual_end - actual_start).total_seconds() / 3600
                    daily_total[current_date] += duration

                if hours:
                    if date_str not in booked_hours:
                        booked_hours[date_str] = []
                    booked_hours[date_str].extend(hours)
                    booked_hours[date_str] = sorted(list(set(booked_hours[date_str])))

                current_date += timedelta(days=1)

        # Формируем списки полностью и частично занятых дней на основе суммарной длительности
        booked_dates_full = []
        booked_dates_partial = []

        for date, total_hours in daily_total.items():
            date_str = date.isoformat()
            if total_hours >= 12:  # полный рабочий день (8:00-20:00 = 12 часов)
                booked_dates_full.append(date_str)
            elif total_hours > 0:
                booked_dates_partial.append(date_str)

        context['booked_dates_full'] = json.dumps(booked_dates_full)
        context['booked_dates_partial'] = json.dumps(booked_dates_partial)
        context['booked_hours'] = json.dumps(booked_hours)

        return context