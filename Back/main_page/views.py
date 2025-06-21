from django.shortcuts import render, redirect
from users.models import UserProfile

def main(request):
    # Получаем choices из модели UserProfile
    sickness_choices = UserProfile.SICKNESS_CHOICES
    return render(request, 'flatpages/main_page.html', {'sickness_choices': sickness_choices})

# Create your views here.

def main_page(request):
    sicknesses = UserProfile.objects.values_list('sickness', flat=True).distinct()
    return render(request, 'flatpages/main_page.html', {'sicknesses': sicknesses})
