from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path

from .forms import InfoAbout
from .views import user_login, CustomLogoutView, register, account

app_name='users'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registration/', register, name='registration'),
    path('account/<int:pk>/', account, name='account'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)