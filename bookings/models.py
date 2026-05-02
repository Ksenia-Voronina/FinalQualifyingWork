from django.db import models
from django.conf import settings
from django.urls import reverse
from spaces.models import Space
from decimal import Decimal


class BookingStatus(models.TextChoices):
    """Статусы бронирования"""
    PENDING = 'pending', 'Ожидает подтверждения'
    CONFIRMED = 'confirmed', 'Подтверждено'
    CANCELLED = 'cancelled', 'Отменено'
    COMPLETED = 'completed', 'Завершено'


class Booking(models.Model):
    """Модель бронирования пространства"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Пользователь'
    )
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Пространство'
    )
    event_name = models.CharField(
        max_length=200,
        verbose_name='Название мероприятия'
    )
    event_description = models.TextField(
        blank=True,
        verbose_name='Описание мероприятия'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Дата и время начала'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Дата и время окончания'
    )
    participants_count = models.PositiveIntegerField(
        verbose_name='Количество участников'
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name='Статус'
    )
    special_requests = models.TextField(
        blank=True,
        verbose_name='Особые пожелания'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['status']),
            models.Index(fields=['space', 'start_datetime']),
        ]
        unique_together = ['space', 'start_datetime', 'end_datetime']

    def __str__(self):
        return f'{self.user.username} - {self.space.name} - {self.start_datetime}'

    def get_absolute_url(self):
        return reverse('bookings:detail', args=[self.id])

    @property  # Превращает метод в атрибут (можно потом метод вызывать без скобок)
    def duration_hours(self):
        """Продолжительность в часах (Decimal)"""
        delta = self.end_datetime - self.start_datetime
        return Decimal(str(delta.total_seconds() / 3600))

    @property
    def total_price(self):
        """Общая стоимость"""
        return self.duration_hours * Decimal(str(self.space.price_per_hour))