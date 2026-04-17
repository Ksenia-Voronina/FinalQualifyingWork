from django.db import models
from django.urls import reverse


class Space(models.Model):
    """Модель пространства"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL'
    )
    description = models.TextField(
        verbose_name='Полное описание'
    )
    short_description = models.CharField(
        max_length=200,
        verbose_name='Краткое описание'
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Вместимость (человек)'
    )
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена за час (₽)'
    )
    image = models.ImageField(
        upload_to='spaces/',
        blank=True,
        null=True,
        verbose_name='Главное изображение'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступно для бронирования'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Пространство'
        verbose_name_plural = 'Пространства'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spaces:detail', args=[self.slug])
