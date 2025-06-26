from django.shortcuts import render, redirect
from users.models import UserCard
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def main(request):
    cards = None
    selected_card_id = request.session.get('selected_card_id')
    selected_card = None
    if request.user.is_authenticated:
        cards = UserCard.objects.filter(user=request.user)
        if request.method == 'POST':
            card_id = request.POST.get('card_id')
            if card_id and cards.filter(id=card_id).exists():
                request.session['selected_card_id'] = int(card_id)
                selected_card_id = int(card_id)
                messages.success(request, 'Карточка пользователя выбрана!')
        if selected_card_id:
            selected_card = cards.filter(id=selected_card_id).first()
    return render(request, 'flatpages/main_page.html', {
        'cards': cards,
        'selected_card': selected_card,
    })

# Create your views here.

def main_page(request):
    sicknesses = UserCard.objects.values_list('sickness', flat=True).distinct()
    return render(request, 'flatpages/main_page.html', {'sicknesses': sicknesses})
