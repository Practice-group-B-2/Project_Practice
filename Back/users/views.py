from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.transaction import commit
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import BaseRegisterForm, LoginForm, InfoAbout, UserCardForm
from django.contrib.auth.models import User
from .models import UserProfile, UserCard
from django.views.decorators.csrf import csrf_exempt
import json


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему!')
                    return redirect('main_page:main')
                else:
                    messages.error(request, 'Аккаунт отключен.')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'flatpages/users/login.html', {'form': form})

@login_required
def account(request, pk):
    user = User.objects.get(pk=pk)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Получаем карточки пользователя
    user_cards = UserCard.objects.filter(user=user).order_by('-created_at')
    
    if request.method == 'POST':
        infoForm = InfoAbout(request.POST)
        if infoForm.is_valid():
            profile.height = infoForm.cleaned_data['height']
            profile.weight = infoForm.cleaned_data['weight']
            profile.sickness = infoForm.cleaned_data['sickness']
            profile.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:account', pk=pk)
    else:
        infoForm = InfoAbout(initial={
            'height': profile.height,
            'weight': profile.weight,
            'sickness': profile.sickness
        })
    
    return render(request, 'flatpages/users/account.html', {
        'form': infoForm,
        'profile': profile,
        'user': user,
        'user_cards': user_cards
    })

@csrf_exempt
@login_required
def create_user_card_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = UserCardForm(data)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return JsonResponse({
                'success': True,
                'message': 'Карточка успешно создана!',
                'card': {
                    'id': card.id,
                    'name': card.name,
                    'height': card.height,
                    'weight': str(card.weight),
                    'sickness': card.sickness,
                    'sickness_display': card.get_sickness_display()
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

@csrf_exempt
@login_required
def edit_user_card_ajax(request, card_id):
    try:
        card = UserCard.objects.get(id=card_id, user=request.user)
    except UserCard.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Карточка не найдена'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        form = UserCardForm(data, instance=card)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Карточка успешно обновлена!',
                'card': {
                    'id': card.id,
                    'name': card.name,
                    'height': card.height,
                    'weight': str(card.weight),
                    'sickness': card.sickness,
                    'sickness_display': card.get_sickness_display()
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

@login_required
def delete_user_card_ajax(request, card_id):
    try:
        card = UserCard.objects.get(id=card_id, user=request.user)
        card.delete()
        return JsonResponse({
            'success': True,
            'message': 'Карточка успешно удалена!'
        })
    except UserCard.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Карточка не найдена'
        })

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main_page:main')  # Явно указываем страницу для перенаправления
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)

def register(request):
    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Создаем профиль пользователя
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('main_page:main')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BaseRegisterForm()
    
    return render(request, 'flatpages/users/registration.html', {'form': form})

