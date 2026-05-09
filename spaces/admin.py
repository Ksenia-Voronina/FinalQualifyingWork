from django.contrib import admin
from .models import Space


@admin.register(Space)  # Регистрирует модель Space в админке.
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'price_per_hour', 'show_on_homepage', 'is_available']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price_per_hour', 'show_on_homepage', 'is_available']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Характеристики', {
            'fields': ('capacity', 'price_per_hour', 'is_available')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
    )