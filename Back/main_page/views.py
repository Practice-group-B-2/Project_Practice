from django.shortcuts import render, redirect
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def main(request):
    profiles = None
    selected_profile_id = request.session.get('selected_profile_id')
    selected_profile = None
    if request.user.is_authenticated:
        profiles = UserProfile.objects.filter(user=request.user)
        if request.method == 'POST':
            profile_id = request.POST.get('profile_id')
            if profile_id and profiles.filter(id=profile_id).exists():
                request.session['selected_profile_id'] = int(profile_id)
                selected_profile_id = int(profile_id)
                messages.success(request, 'Профиль выбран!')
        if selected_profile_id:
            selected_profile = profiles.filter(id=selected_profile_id).first()
    return render(request, 'flatpages/main_page.html', {
        'profiles': profiles,
        'selected_profile': selected_profile,
    })

# Create your views here.

def main_page(request):
    sicknesses = UserProfile.objects.values_list('sickness', flat=True).distinct()
    return render(request, 'flatpages/main_page.html', {'sicknesses': sicknesses})
