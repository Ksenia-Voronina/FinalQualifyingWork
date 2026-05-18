import threading
from django.core.mail import send_mail
from django.conf import settings


class EmailThread(threading.Thread):
    """Класс для асинхронной отправки писем в отдельном потоке"""

    def __init__(self, subject, message, from_email, recipient_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            # Логируем ошибку, но не прерываем выполнение
            print(f'Ошибка отправки письма: {e}')


def send_email_async(subject, message, recipient_list):
    """Отправляет письмо асинхронно"""
    EmailThread(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list).start()