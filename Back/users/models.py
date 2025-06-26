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
        default=170 
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
        default=70.0 
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles',
        help_text='Имя',
    )
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




class profile_Status(models.Model):
    Profile_Status=(
        ("Doctor","Доктор"),
        ("Helper","Помошник"),
        ("Patient","Пациент")
    )

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cards')
    name = models.CharField(
        max_length=100, 
        verbose_name='Имя',
        help_text='Введите имя'
    )
    height = models.PositiveIntegerField(
        validators=[
            MinValueValidator(100, message='Рост не может быть меньше 100 см'),
            MaxValueValidator(250, message='Рост не может быть больше 250 см')
        ],
        verbose_name='Рост (см)',
        help_text='Введите рост в сантиметрах',
        default=170
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[
            MinValueValidator(30, message='Вес не может быть меньше 30 кг'),
            MaxValueValidator(300, message='Вес не может быть больше 300 кг')
        ],
        verbose_name='Вес (кг)',
        help_text='Введите вес в килограммах',
        default=70.0
    )
    sickness = models.CharField(
        max_length=50,
        choices=UserProfile.SICKNESS_CHOICES,
        default='none',
        verbose_name='Заболевание'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Карточка {self.name} пользователя {self.user.username}'

    def get_sickness_display(self):
        sickness_map = {
            'diabetes': 'Диабет',
            'celiac': 'Целиакия',
            'phenylketonuria': 'Фенилкетонурия',
            'lactose': 'Непереносимость лактозы',
            'none': 'Нет заболеваний'
        }
        return sickness_map.get(self.sickness, 'Нет заболеваний')

    class Meta:
        verbose_name = 'Карточка пользователя'
        verbose_name_plural = 'Карточки пользователей'