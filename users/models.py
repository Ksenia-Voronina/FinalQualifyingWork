from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Расширение модели пользователя"""

    FACULTY_CHOICES = [
        ('fkti', 'ФКТИ'),
        ('frt', 'ФРТ'),
        ('fea', 'ФЭА'),
        ('fibs', 'ФИБС'),
        ('gf', 'ГФ'),
        ('inprotech', 'ИНПРОТЕХ'),
    ]

    COURSE_CHOICES = [
        # Бакалавриат / Специалитет
        ('b1', '1 курс (бакалавриат/специалитет)'),
        ('b2', '2 курс (бакалавриат/специалитет)'),
        ('b3', '3 курс (бакалавриат/специалитет)'),
        ('b4', '4 курс (бакалавриат/специалитет)'),
        ('s5', '5 курс (специалитет)'),
        # Магистратура
        ('m1', '1 курс (магистратура)'),
        ('m2', '2 курс (магистратура)'),
        # Аспирантура
        ('postgrad', 'аспирантура'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    student_id = models.CharField(
        max_length=6,
        blank=True,
        verbose_name='Студенческий билет'
    )
    faculty = models.CharField(
        max_length=20,
        choices=FACULTY_CHOICES,
        blank=True,
        verbose_name='Факультет'
    )
    course = models.PositiveSmallIntegerField(
        choices=COURSE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Курс'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматическое создание профиля при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматическое сохранение профиля при сохранении пользователя"""
    instance.profile.save()