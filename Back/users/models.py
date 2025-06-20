from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    SICKNESS_CHOICES = (
        ('diabetes', 'Сахарный диабет'),
        ('celiac', 'Целиакия'),
        ('phenylketonuria', 'Фенилкетонурия'),
        ('lactose', 'Непереносимость лактозы'),
        ('none', 'Нет заболеваний'),
    )
    height = models.PositiveIntegerField(
        validators=[
            MinValueValidator(100, message='Рост не может быть меньше 100 см'),
            MaxValueValidator(250, message='Рост не может быть больше 250 см')
        ],
        verbose_name='Рост (см)',
        help_text='Введите ваш рост в сантиметрах',
        default=170  # Среднее значение роста
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[
            MinValueValidator(30, message='Вес не может быть меньше 30 кг'),
            MaxValueValidator(300, message='Вес не может быть больше 300 кг')
        ],
        verbose_name='Вес (кг)',
        help_text='Введите ваш вес в килограммах',
        default=70.0  # Среднее значение веса
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sickness = models.CharField(
        max_length=50,
        choices=SICKNESS_CHOICES,
        default='none',
        verbose_name='Заболевание'
    )
    
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Profile_Status(models.Model):
    Profile_Status=(
        ("Doctor","Доктор"),
        ("Helper","Помошник"),
        ("Patient","Пациент")
    )