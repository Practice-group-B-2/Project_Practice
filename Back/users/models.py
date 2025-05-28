from django.db import models

class User(models.Model):
    SICKNESS_CHOICES = (
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('black', 'black'),
        ('white', 'white')
    )
    email = models.EmailField()
    username = models.

# Create your models here.
