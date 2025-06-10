from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import BaseRegisterForm, LoginForm, InfoAbout
from django.contrib.auth.models import User
from .models import UserProfile


def user_login(request):
    Loginform = LoginForm(request.POST)
    if request.method == 'POST':

        if Loginform.is_valid():
            cd = Loginform.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main_page:main')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login.')
                return render(request, 'flatpages/users/login.html', {})
    return render(request, 'flatpages/users/login.html', {'Loginform': Loginform})
@login_required
def account(request, pk):
    user = User.objects.get(pk=pk)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
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
        'user': user
    })



# Create your views here.
class Logout(LoginView):
    def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("main:homepage")

def register(request):
    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('main_page:main')
    else:
        form = BaseRegisterForm()

    return render(request, 'flatpages/users/registration.html', {'form': form})

