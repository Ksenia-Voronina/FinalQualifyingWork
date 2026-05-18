from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'reply_button', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at']

    def reply_button(self, obj):
        """Кнопка для ответа пользователю (открывает почтовый клиент)"""
        return format_html(
            '<a href="{}" target="_blank" '
            'style="background-color: #1e3799; color: white; padding: 4px 10px; '
            'border-radius: 4px; text-decoration: none; font-size: 12px; '
            'display: inline-block;">'
            '✉️Ответить</a>',
            obj.get_mailto_link()
        )

    reply_button.short_description = 'Ответить'

    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'email')
        }),
        ('Сообщение', {
            'fields': ('subject', 'message')
        }),
        ('Статус', {
            'fields': ('status', 'created_at')
        }),
    )