from django.db import models
from urllib.parse import quote


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('read', 'Прочитано'),
        ('replied', 'Ответ отправлен'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Сообщение от {self.name} - {self.created_at.strftime("%d.%m.%Y")}'

    def get_mailto_link(self):
        """Формирует mailto ссылку для открытия почтового клиента"""
        encoded_subject = quote(f'Re: {self.subject}')
        encoded_body = quote(f'Здравствуйте, {self.name}!\n\nБлагодарим за ваше сообщение.\n\n')
        return f'mailto:{self.email}?subject={encoded_subject}&body={encoded_body}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']