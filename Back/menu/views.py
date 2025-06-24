from django.shortcuts import render
import random
from django.utils import timezone
from users.models import UserProfile
from sugar_diabet.views import recipes

def get_profile_for_menu(request):
    profile = None
    if request.user.is_authenticated:
        selected_profile_id = request.session.get('selected_profile_id')
        if selected_profile_id:
            try:
                profile = UserProfile.objects.get(id=selected_profile_id, user=request.user)
            except UserProfile.DoesNotExist:
                pass
    return profile

def filter_recipes_by_health(profile):
    filtered = []
    if not profile:
        return recipes
    for r in recipes:
        if profile.sickness == 'diabetes' and not r.get('diabetic', False):
            continue
        filtered.append(r)
    return filtered

def generate_menu_for_week(profile):
    filtered_recipes = filter_recipes_by_health(profile)
    menu = []
    meal_types = ['breakfast', 'lunch', 'dinner']
    for day in range(7):
        day_menu = {}
        random.shuffle(filtered_recipes)
        for i, meal in enumerate(meal_types):
            recipe = filtered_recipes[(day*3 + i) % len(filtered_recipes)]
            day_menu[meal] = recipe
        menu.append(day_menu)
    return menu

def menu_view(request):
    today = timezone.localdate()
    day_param = request.GET.get('day')
    if day_param is not None and day_param.isdigit():
        day_index = int(day_param)
        if not (0 <= day_index <= 6):
            day_index = today.weekday()
    else:
        day_index = today.weekday()
    profile = get_profile_for_menu(request)
    if 'weekly_menu' not in request.session:
        request.session['weekly_menu'] = None
    if not request.session['weekly_menu']:
        weekly_menu = generate_menu_for_week(profile)
        request.session['weekly_menu'] = weekly_menu
    else:
        weekly_menu = request.session['weekly_menu']
    if profile and request.session.get('menu_profile_id') != (profile.id if profile else None):
        weekly_menu = generate_menu_for_week(profile)
        request.session['weekly_menu'] = weekly_menu
        request.session['menu_profile_id'] = profile.id if profile else None
    day_menu = weekly_menu[day_index]
    summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for meal in day_menu.values():
        summary['calories'] += meal['nutrition']['calories']
        summary['protein'] += meal['nutrition']['protein']
        summary['carbs'] += meal['nutrition']['carbs']
        summary['fat'] += meal['nutrition']['fat']
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    yesterday_index = (day_index - 1) % 7
    tomorrow_index = (day_index + 1) % 7
    return render(request, 'flatpages/menu/menu.html', {
        'day_menu': day_menu,
        'summary': summary,
        'day_index': day_index,
        'week_days': week_days,
        'yesterday_index': yesterday_index,
        'tomorrow_index': tomorrow_index,
    })
# Create your views here.
