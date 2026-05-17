from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    """Форма создания бронирования"""

    class Meta:
        model = Booking
        fields = ['event_name', 'event_description', 'start_datetime', 'end_datetime',
                  'participants_count', 'special_requests']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_description': forms.Textarea(attrs={'rows': 4}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'event_name': 'Название мероприятия',
            'event_description': 'Описание мероприятия',
            'start_datetime': 'Дата и время начала',
            'end_datetime': 'Дата и время окончания',
            'participants_count': 'Количество участников',
            'special_requests': 'Особые пожелания',
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем параметр space, если он передан
        self.space = kwargs.pop('space', None)
        super().__init__(*args, **kwargs)

    def clean_start_datetime(self):
        """Проверка, что дата начала не в прошлом и в рабочее время"""
        start = self.cleaned_data.get('start_datetime')

        if start and start < timezone.now():
            raise forms.ValidationError('Нельзя выбрать дату и время в прошлом')

        # Проверка рабочего времени (с 8:00 до 20:00)
        if start:
            hour = start.hour
            if hour < 8 or hour >= 20:
                raise forms.ValidationError('Пространство доступно для бронирования только с 8:00 до 20:00')

        return start

    def clean_end_datetime(self):
        """Проверка, что время окончания в рабочее время"""
        end = self.cleaned_data.get('end_datetime')

        if end:
            hour = end.hour
            # Если окончание в 20:00 — это допустимо (последний час)
            if hour < 8 or hour > 20:
                raise forms.ValidationError('Пространство доступно для бронирования только до 20:00')
            if hour == 20 and end.minute > 0:
                raise forms.ValidationError('Время окончания не может быть позже 20:00')

        return end

    def clean(self):
        """Общая проверка формы"""
        cleaned_data = super().clean()
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')
        space = self.space

        if start and end and space:
            overlapping = Booking.objects.filter(
                space=space,
                status__in=['pending', 'confirmed'],
                end_datetime__gt=start,
                start_datetime__lt=end
            ).exclude(id=self.instance.pk if self.instance.pk else None)

            if overlapping.exists():
                self.add_error('end_datetime', 'Выбранное время занято. Пожалуйста, выберите другой интервал.')

        if start and end and start >= end:
            self.add_error('end_datetime', 'Время окончания должно быть позже времени начала')

        return cleaned_data
