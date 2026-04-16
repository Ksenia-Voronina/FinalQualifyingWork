from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'faculty', 'course', 'student_id']
    search_fields = ['user__username', 'user__email', 'phone', 'student_id']
    list_filter = ['faculty', 'course']
    list_editable = ['phone', 'faculty', 'course']

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'phone', 'student_id')
        }),
        ('Учебная информация', {
            'fields': ('faculty', 'course')
        }),
        ('Аватар', {
            'fields': ('avatar',)
        }),
    )