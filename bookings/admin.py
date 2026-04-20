from django.contrib import admin
from .models import Booking


@admin.register(Booking)   # Регистрирует модель Booking в админ-панели Django
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'space', 'start_datetime', 'end_datetime', 'status', 'created_at']
    list_filter = ['status', 'space', 'created_at']
    search_fields = ['user__username', 'user__email', 'event_name', 'space__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Информация о мероприятии', {
            'fields': ('user', 'space', 'event_name', 'event_description', 'participants_count')
        }),
        ('Время бронирования', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Дополнительно', {
            'fields': ('special_requests', 'status')
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )