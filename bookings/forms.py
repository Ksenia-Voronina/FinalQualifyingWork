from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    """Форма создания бронирования"""

    time_slot = forms.ChoiceField(
        choices=[],
        required=False,
        label='Доступное время'
    )

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
        self.space = kwargs.pop('space', None)
        super().__init__(*args, **kwargs)

        # Добавляем поле time_slot
        if self.space:
            self.fields['time_slot'].choices = self.get_available_slots()

    def get_available_slots(self, date=None):
        """Получение доступных слотов на определённую дату"""
        from spaces.models import Space

        if date is None:
            date = timezone.now().date()

        WORK_START = 8
        WORK_END = 20
        SLOT_DURATION = 2  # длительность слота в часах

        # Получаем занятые интервалы на выбранную дату
        booked = Booking.objects.filter(
            space=self.space,
            status__in=['pending', 'confirmed'],
            start_datetime__date=date
        )

        booked_hours = set()
        for b in booked:
            start_hour = b.start_datetime.hour
            end_hour = b.end_datetime.hour
            for hour in range(start_hour, end_hour):
                booked_hours.add(hour)

        # Формируем доступные слоты
        choices = [('', '---------')]
        for hour in range(WORK_START, WORK_END - SLOT_DURATION + 1):
            is_booked = any(h in booked_hours for h in range(hour, hour + SLOT_DURATION))
            slot_label = f"{hour:02d}:00 - {hour + SLOT_DURATION:02d}:00"
            if not is_booked:
                choices.append((slot_label, slot_label))

        return choices


    def clean_start_datetime(self):
        """Проверка, что дата начала не в прошлом"""
        start = self.cleaned_data.get('start_datetime')

        if start and start < timezone.now():
            raise forms.ValidationError('Нельзя выбрать дату и время в прошлом')

        return start

    def clean(self):
        """Проверка, что время не пересекается с существующими бронированиями"""
        cleaned_data = super().clean()
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')
        space = self.space

        # Если пространство ещё не привязано (новая запись), берём из cleaned_data
        if not space and 'space' in self.data:
            from spaces.models import Space
            try:
                space_id = self.data.get('space')
                space = Space.objects.get(id=space_id)
            except:
                pass

        if start and end and space:
            # Проверяем пересечение с существующими бронированиями
            overlapping = Booking.objects.filter(
                space=space,
                status__in=['pending', 'confirmed'],  # только активные брони
                end_datetime__gt=start,
                start_datetime__lt=end
            ).exclude(id=self.instance.pk if self.instance.pk else None)

            if overlapping.exists():
                self.add_error('end_datetime', 'Выбранное время занято. Пожалуйста, выберите другой интервал.')

        if start and end and start >= end:
            self.add_error('end_datetime', 'Время окончания должно быть позже времени начала')

        return cleaned_data