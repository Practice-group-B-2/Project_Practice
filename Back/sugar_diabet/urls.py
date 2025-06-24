from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path

from .views import calculator123, calculate_nutrition

app_name='calculator'
urlpatterns = [
    path('', calculator123, name='calculator'),
    path('calculate-nutrition/', calculate_nutrition, name='calculate_nutrition'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)