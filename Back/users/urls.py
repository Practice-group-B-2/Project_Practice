from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path

from .forms import InfoAbout
from .views import *

app_name='users'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registration/', register, name='registration'),
    path('account/<int:pk>/', account, name='account'),
    path('create-card/', create_user_card_ajax, name='create_user_card'),
    path('edit-card/<int:card_id>/', edit_user_card_ajax, name='edit_user_card'),
    path('delete-card/<int:card_id>/', delete_user_card_ajax, name='delete_user_card'),
    path('create-card-ajax/', create_user_card_ajax, name='create_user_card_ajax'),
    path('edit-card-ajax/<int:card_id>/', edit_user_card_ajax, name='edit_user_card_ajax'),
    path('delete-card-ajax/<int:card_id>/', delete_user_card_ajax, name='delete_user_card_ajax'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)