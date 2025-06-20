from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path


from .views import user_login, Logout, register
app_name='users'
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', Logout.as_view(template_name='flatpages/Account123/logout.html'),name='logout'),
    path('registration/',register,name='registration'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)