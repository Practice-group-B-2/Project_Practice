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

        if (disease === 'diabetes' && isDiabetic) priority += 2;
        if (disease === 'hypertension' && isLowSalt) priority += 2;
        if (disease === 'low_salt' && isLowSalt) priority += 2;
        if (weight > 100 && isLowCalorie) priority += 1;
        if (age > 60 && isLowSalt) priority += 1;

        if (disease === 'diabetes' && !isDiabetic) shouldDisplay = false;
        if (disease === 'hypertension' && !isLowSalt) shouldDisplay = false;
        if (disease === 'low_salt' && !isLowSalt) shouldDisplay = false;
        if (weight > 100 && !isLowCalorie) shouldDisplay = false;

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
    if (!currentRecipe || !weight) return;

    const csrftoken = getCookie('csrftoken');

    fetch(CALCULATE_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ recipe: currentRecipe, weight: weight })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            document.getElementById('calories').textContent = data.calories;
            document.getElementById('protein').textContent = data.protein;
            document.getElementById('carbs').textContent = data.carbs;
            document.getElementById('fat').textContent = data.fat;
            document.getElementById('nutritionResults').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
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