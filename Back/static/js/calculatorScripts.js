// static/js/scripts.js
document.addEventListener('DOMContentLoaded', () => {
    showWelcomeModal();
    setupEventListeners();
});

let currentRecipe = null;

function showWelcomeModal() {
    document.getElementById('welcomeModal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
}

function closeWelcomeModal() {
    document.getElementById('welcomeModal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
    recommendRecipes();
}

function recommendRecipes() {
    const age = parseInt(document.getElementById('ageSlider').value);
    const weight = parseInt(document.getElementById('weightInput').value);
    const disease = document.getElementById('diseaseSelect').value;

    document.querySelectorAll('.trade-item').forEach(item => {
        const isDiabetic = item.dataset.diabetic === 'true';
        const isLowCalorie = item.dataset.lowCalorie === 'true';
        const isLowSalt = item.dataset.lowSalt === 'true';

        let priority = 0;
        let shouldDisplay = true;

        // Логика для сахарного диабета
        if (disease === 'diabetes' && isDiabetic) priority += 3;
        if (disease === 'diabetes' && !isDiabetic) shouldDisplay = false;

        // Логика для целиакии (безглютеновая диета)
        if (disease === 'celiac') {
            // Предполагаем, что супы и овощные блюда обычно безопасны
            const safeCategories = ['Суп', 'Салат', 'Рагу'];
            const itemCategory = item.dataset.category;
            if (safeCategories.includes(itemCategory)) {
                priority += 2;
            } else {
                shouldDisplay = false; // Исключаем блюда с глютеном
            }
        }

        // Логика для фенилкетонурии (низкобелковая диета)
        if (disease === 'phenylketonuria') {
            // Предпочитаем низкокалорийные блюда с меньшим содержанием белка
            if (isLowCalorie) priority += 2;
            // Исключаем блюда с высоким содержанием белка (рыба, мясо)
            const highProteinCategories = ['Рыба', 'Жаркое'];
            const itemCategory = item.dataset.category;
            if (highProteinCategories.includes(itemCategory)) {
                shouldDisplay = false;
            }
        }

        // Логика для непереносимости лактозы
        if (disease === 'lactose') {
            // Предпочитаем овощные блюда и супы
            const safeCategories = ['Суп', 'Салат', 'Рагу'];
            const itemCategory = item.dataset.category;
            if (safeCategories.includes(itemCategory)) {
                priority += 2;
            }
            // Исключаем блюда, которые могут содержать молочные продукты
            const dairyCategories = ['Жаркое']; // Упрощенно
            if (dairyCategories.includes(itemCategory)) {
                shouldDisplay = false;
            }
        }

        // Общие рекомендации по весу и возрасту
        if (weight > 100 && isLowCalorie) priority += 1;
        if (age > 60 && isLowSalt) priority += 1;

        item.style.display = shouldDisplay ? 'block' : 'none';

        item.classList.remove('priority-high', 'priority-medium');
        if (priority >= 3) {
            item.classList.add('priority-high');
        } else if (priority >= 1) {
            item.classList.add('priority-medium');
        }
    });

    const container = document.querySelector('.trade-list');
    const items = Array.from(container.querySelectorAll('.trade-item[style*="block"]'));

    items.sort((a, b) => {
        const aPriority = a.classList.contains('priority-high') ? 2 :
                         a.classList.contains('priority-medium') ? 1 : 0;
        const bPriority = b.classList.contains('priority-high') ? 2 :
                         b.classList.contains('priority-medium') ? 1 : 0;
        return bPriority - aPriority;
    });

    items.forEach(item => container.appendChild(item));
}

function filterRecipes() {
    const category = document.getElementById('filterDropdown').value;
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    document.querySelectorAll('.trade-item').forEach(item => {
        const itemCategory = item.dataset.category;
        const itemName = item.querySelector('.item-name').textContent.toLowerCase();
        const categoryMatch = category === 'all' || itemCategory === category;
        const searchMatch = itemName.includes(searchTerm);

        item.style.display = categoryMatch && searchMatch ? 'block' : 'none';
    });
}

function showRecipeModal(videoUrl, title, description) {
    document.getElementById('modal-recipe-title').textContent = title;
    document.getElementById('modal-recipe-description').textContent = description;
    document.getElementById('modal-recipe-video').src = videoUrl;
    document.querySelector('.recipe-modal').style.display = 'block';
}

function closeRecipeModal() {
    document.querySelector('.recipe-modal').style.display = 'none';
    document.getElementById('modal-recipe-video').src = '';
}

function showCalculator(recipeName) {
    document.getElementById('calculatorModal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
    currentRecipe = recipeName;
    document.getElementById('nutritionResults').style.display = 'none';
}

function closeCalculatorModal() {
    document.getElementById('calculatorModal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
}

function calculateNutrition() {
    const weight = document.getElementById('portionWeight').value;
    const disease = document.getElementById('calculatorDiseaseSelect').value;
    if (!currentRecipe || !weight) return;

    const csrftoken = getCookie('csrftoken');

    const formData = new FormData();
    formData.append('recipe', currentRecipe);
    formData.append('weight', weight);
    formData.append('disease', disease);

    fetch(CALCULATE_URL, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            document.getElementById('calories').textContent = data.calories;
            document.getElementById('protein').textContent = data.protein;
            document.getElementById('carbs').textContent = data.carbs;
            document.getElementById('fat').textContent = data.fat;
            
            // Генерируем рекомендации на основе болезни
            const recommendations = generateDiseaseRecommendations(disease, data);
            document.getElementById('recommendationText').textContent = recommendations;
            
            document.getElementById('nutritionResults').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function generateDiseaseRecommendations(disease, nutritionData) {
    const calories = parseFloat(nutritionData.calories);
    const protein = parseFloat(nutritionData.protein);
    const carbs = parseFloat(nutritionData.carbs);
    const fat = parseFloat(nutritionData.fat);

    let recommendations = '';

    switch(disease) {
        case 'diabetes':
            if (carbs > 30) {
                recommendations = '⚠️ Высокое содержание углеводов. Рекомендуется уменьшить порцию или выбрать альтернативное блюдо.';
            } else if (carbs > 20) {
                recommendations = '⚠️ Умеренное содержание углеводов. Следите за общим потреблением углеводов в течение дня.';
            } else {
                recommendations = '✅ Подходящее содержание углеводов для диабетиков.';
            }
            break;

        case 'phenylketonuria':
            if (protein > 10) {
                recommendations = '⚠️ Высокое содержание белка. Не рекомендуется при фенилкетонурии.';
            } else if (protein > 5) {
                recommendations = '⚠️ Умеренное содержание белка. Ограничьте потребление.';
            } else {
                recommendations = '✅ Низкое содержание белка, подходит для диеты при фенилкетонурии.';
            }
            break;

        case 'celiac':
            recommendations = '✅ Это блюдо не содержит глютен и безопасно при целиакии.';
            break;

        case 'lactose':
            recommendations = '✅ Это блюдо не содержит молочные продукты и безопасно при непереносимости лактозы.';
            break;

        case 'none':
        default:
            if (calories > 300) {
                recommendations = '⚠️ Высокая калорийность. Рекомендуется для активных людей.';
            } else if (calories > 200) {
                recommendations = '✅ Умеренная калорийность, подходит для большинства людей.';
            } else {
                recommendations = '✅ Низкая калорийность, отлично подходит для диеты.';
            }
            break;
    }

    return recommendations;
}

function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', filterRecipes);
    document.getElementById('filterDropdown').addEventListener('change', filterRecipes);
    document.getElementById('ageSlider').addEventListener('input', function() {
        document.getElementById('ageValue').textContent = this.value;
    });

    document.querySelector('.modal-overlay').addEventListener('click', function() {
        closeWelcomeModal();
        closeRecipeModal();
        closeCalculatorModal();
    });
}