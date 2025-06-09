        document.addEventListener('DOMContentLoaded', function() {
            const userTypeBtn = document.getElementById('userTypeBtn');
            const userTypeMenu = document.getElementById('userTypeMenu');
            const currentValue = document.getElementById('currentValue');

            userTypeBtn.addEventListener('click', function(event) {
                event.stopPropagation(); 
                userTypeMenu.style.display = userTypeMenu.style.display === 'block' ? 'none' : 'block';
            });

            userTypeMenu.querySelectorAll('div').forEach(option => {
                option.addEventListener('click', function(event) {
                    const selectedValue = this.getAttribute('data-value');
                    currentValue.textContent = `Текущий тип пользователя: ${selectedValue}`; // Обновить текст под кнопкой
                    userTypeMenu.style.display = 'none';а
                });
            });

            document.addEventListener('click', function(event) {
                if (!userTypeBtn.contains(event.target) && !userTypeMenu.contains(event.target)) {
                    userTypeMenu.style.display = 'none'; 
                }
            });
        });