from .views import menu_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path
app_name='menu_url'
urlpatterns = [
    path('', menu_view, name='menu'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)