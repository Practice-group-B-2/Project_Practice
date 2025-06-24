from .views import menu_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path
from . import views
app_name='menu_url'
urlpatterns = [
    path('', menu_view, name='menu'),
    path('allowed_recipes/', views.allowed_recipes, name='allowed_recipes'),
    path('add_recipe_to_meal/', views.add_recipe_to_meal, name='add_recipe_to_meal'),
    path('selected_recipes_for_meal/', views.selected_recipes_for_meal, name='selected_recipes_for_meal'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)