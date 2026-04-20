from django import forms
from .models import Booking
from spaces.models import Space


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

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')

        if start and end:
            if start >= end:
                raise forms.ValidationError('Время окончания должно быть позже времени начала')

        return cleaned_data