from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path

from .views import main
app_name='main_page'
urlpatterns = [
    path('', main, name='main'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
