# main_page/views.py
import random
from django.shortcuts import render
from django.http import JsonResponse

recipes = [
    {
        "name": "Куриный суп",
        "image": "chicken_soup.png",
        "description": "Питательный куриный суп с лапшой.",
        "category": "Суп",
        "diabetic": True,
        "low_calorie": False,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=qhH131jxdvQ",
        "nutrition": {"calories": 150, "protein": 12, "carbs": 10, "fat": 5}
    },
    {
        "name": "Овощной суп",
        "image": "vegetable_soup.png",
        "description": "Вкусный и полезный овощной суп.",
        "category": "Суп",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example2",
        "nutrition": {"calories": 80, "protein": 3, "carbs": 12, "fat": 2}
    },
    {
        "name": "Томатный суп",
        "image": "tomato_soup.png",
        "description": "Классический томатный суп с базиликом.",
        "category": "Суп",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": False,
        "video_url": "https://www.youtube.com/watch?v=example3",
        "nutrition": {"calories": 90, "protein": 2, "carbs": 15, "fat": 3}
    },
    {
        "name": "Тыквенный суп",
        "image": "pumpkin_soup.png",
        "description": "Кремовый тыквенный суп с имбирем.",
        "category": "Суп",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example4",
        "nutrition": {"calories": 100, "protein": 2, "carbs": 18, "fat": 3}
    },
    {
        "name": "Грибной суп",
        "image": "mushroom_soup.png",
        "description": "Кремовый грибной суп с зеленью.",
        "category": "Суп",
        "diabetic": True,
        "low_calorie": False,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example5",
        "nutrition": {"calories": 120, "protein": 4, "carbs": 8, "fat": 8}
    },
    {
        "name": "Салат Цезарь",
        "image": "caesar_salad.png",
        "description": "Классический салат Цезарь с курицей.",
        "category": "Салат",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": False,
        "video_url": "https://www.youtube.com/watch?v=example6",
        "nutrition": {"calories": 350, "protein": 25, "carbs": 20, "fat": 20}
    },
    {
        "name": "Греческий салат",
        "image": "greek_salad.png",
        "description": "Свежий греческий салат с оливками и сыром фета.",
        "category": "Салат",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example7",
        "nutrition": {"calories": 200, "protein": 6, "carbs": 10, "fat": 15}
    },
    {
        "name": "Салат с тунцом",
        "image": "tuna_salad.png",
        "description": "Салат с тунцом, яйцами и овощами.",
        "category": "Салат",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example8",
        "nutrition": {"calories": 180, "protein": 20, "carbs": 5, "fat": 9}
    },
    {
        "name": "Запеченный лосось",
        "image": "baked_salmon.png",
        "description": "Лосось, запеченный с лимоном и травами.",
        "category": "Рыба",
        "diabetic": True,
        "low_calorie": False,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example9",
        "nutrition": {"calories": 250, "protein": 25, "carbs": 0, "fat": 16}
    },
    {
        "name": "Куриные котлеты",
        "image": "chicken_patties.png",
        "description": "Нежные куриные котлеты с овощами.",
        "category": "Жаркое",
        "diabetic": False,
        "low_calorie": False,
        "low_salt": False,
        "video_url": "https://www.youtube.com/watch?v=example10",
        "nutrition": {"calories": 280, "protein": 22, "carbs": 15, "fat": 15}
    },
    {
        "name": "Стейк с овощами",
        "image": "steak_with_vegetables.png",
        "description": "Сочный стейк с запеченными овощами.",
        "category": "Жаркое",
        "diabetic": False,
        "low_calorie": False,
        "low_salt": False,
        "video_url": "https://www.youtube.com/watch?v=example11",
        "nutrition": {"calories": 400, "protein": 30, "carbs": 20, "fat": 25}
    },
    {
        "name": "Овощное рагу",
        "image": "vegetable_ragout.png",
        "description": "Рагу из свежих овощей с травами.",
        "category": "Рагу",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example12",
        "nutrition": {"calories": 120, "protein": 3, "carbs": 20, "fat": 4}
    },
    {
        "name": "Запеченные овощи",
        "image": "roasted_vegetables.png",
        "description": "Ассорти из запеченных овощей с травами.",
        "category": "Рагу",
        "diabetic": True,
        "low_calorie": True,
        "low_salt": True,
        "video_url": "https://www.youtube.com/watch?v=example13",
        "nutrition": {"calories": 100, "protein": 2, "carbs": 15, "fat": 4}
    }
]


def main_page(request):
    random.shuffle(recipes)
    return render(request, 'main_page.html', {'trade_items': recipes})


def calculate_nutrition(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe')
        weight = float(data.get('weight', 100))

        recipe = next((r for r in recipes if r['name'] == recipe_name), None)
        if not recipe:
            return JsonResponse({"error": "Рецепт не найден"}, status=404)

        ratio = weight / 100
        nutrition = recipe['nutrition']
        calculated = {
            "calories": round(nutrition["calories"] * ratio, 1),
            "protein": round(nutrition["protein"] * ratio, 1),
            "carbs": round(nutrition["carbs"] * ratio, 1),
            "fat": round(nutrition["fat"] * ratio, 1)
        }

        return JsonResponse(calculated)

    return JsonResponse({"error": "Invalid request method"}, status=400)