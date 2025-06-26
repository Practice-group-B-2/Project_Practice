from django.shortcuts import render
import random
from django.utils import timezone
from users.models import UserCard
from sugar_diabet.views import recipes
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def get_card_for_menu(request):
    card = None
    if request.user.is_authenticated:
        selected_card_id = request.session.get('selected_card_id')
        if selected_card_id:
            try:
                card = UserCard.objects.get(id=selected_card_id, user=request.user)
            except UserCard.DoesNotExist:
                pass
    return card

def filter_recipes_by_health(card):
    filtered = []
    if not card:
        return recipes
    for r in recipes:
        if card.sickness == 'diabetes' and not r.get('diabetic', False):
            continue
        filtered.append(r)
    return filtered

def generate_menu_for_week(card):
    filtered_recipes = filter_recipes_by_health(card)
    menu = []
    meal_types = ['breakfast', 'lunch', 'dinner']
    for day in range(7):
        day_menu = {}
        random.shuffle(filtered_recipes)
        for i, meal in enumerate(meal_types):
            recipe = filtered_recipes[(day*3 + i) % len(filtered_recipes)]
            day_menu[meal] = [recipe]
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
    card = get_card_for_menu(request)
    if 'weekly_menu' not in request.session:
        request.session['weekly_menu'] = None
    if not request.session['weekly_menu']:
        weekly_menu = generate_menu_for_week(card)
        request.session['weekly_menu'] = weekly_menu
    else:
        weekly_menu = request.session['weekly_menu']
    if card and request.session.get('menu_card_id') != (card.id if card else None):
        weekly_menu = generate_menu_for_week(card)
        request.session['weekly_menu'] = weekly_menu
        request.session['menu_card_id'] = card.id if card else None
    day_menu = weekly_menu[day_index]
    summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for meal in day_menu.values():
        if isinstance(meal, list):
            for recipe in meal:
                summary['calories'] += recipe['nutrition']['calories']
                summary['protein'] += recipe['nutrition']['protein']
                summary['carbs'] += recipe['nutrition']['carbs']
                summary['fat'] += recipe['nutrition']['fat']
        else:
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
        'recipies': recipes,
    })

@require_GET
def allowed_recipes(request):
    card = get_card_for_menu(request)
    allowed = filter_recipes_by_health(card)
    return JsonResponse({'recipes': [
        {'id': i, 'name': r['name']} for i, r in enumerate(allowed)
    ]})

@csrf_exempt  
@require_POST
def add_recipe_to_meal(request):
    data = json.loads(request.body)
    meal = data.get('meal')  
    recipe_id = data.get('recipe_id')
    checked = data.get('checked')
    card = get_card_for_menu(request)
    allowed = filter_recipes_by_health(card)
    weekly_menu = request.session.get('weekly_menu')
    day_index = timezone.localdate().weekday()
    if not weekly_menu:
        weekly_menu = generate_menu_for_week(card)
    current = weekly_menu[day_index][meal]
    if not isinstance(current, list):
        current = [current]
    if recipe_id is not None and recipe_id.isdigit() and int(recipe_id) < len(allowed):
        recipe = allowed[int(recipe_id)]
        if checked:
            if recipe not in current:
                current.append(recipe)
        else:
            current = [r for r in current if r != recipe]
    weekly_menu[day_index][meal] = current
    request.session['weekly_menu'] = weekly_menu
    return JsonResponse({'recipes': current})

@require_GET
def selected_recipes_for_meal(request):
    meal = request.GET.get('meal')
    day_index = timezone.localdate().weekday()
    weekly_menu = request.session.get('weekly_menu')
    selected_ids = []
    if weekly_menu and meal in weekly_menu[day_index]:
        selected = weekly_menu[day_index][meal]
        if isinstance(selected, list):
            card = get_card_for_menu(request)
            allowed = filter_recipes_by_health(card)
            selected_ids = [
                str(allowed.index(r)) for r in selected if r in allowed
            ]
    return JsonResponse({'selected_ids': selected_ids})

# Create your views here.
