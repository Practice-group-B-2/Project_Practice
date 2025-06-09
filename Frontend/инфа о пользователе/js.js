//1й выпадющий список
function toggleDropdown() {
    const dropdownContent = document.querySelector('.dropdown__content__diet');
    const icon = document.querySelector('.fa-caret-down'); 

    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
        icon.classList.remove('rotate'); 
    } else {
        dropdownContent.style.display = 'block';
        icon.classList.add('rotate'); 
    }
}

function selectItem(item) {
    document.getElementById('DietInput').value = item; 
    document.querySelector('.dropdown__content__diet').style.display = 'none'; 
    document.querySelector('.fa-caret-down').classList.remove('rotate'); 
}

window.onclick = function(event) {
    if (!event.target.matches('#DietInput') && !event.target.matches('.icon')) {
        const dropdownContent = document.querySelector('.dropdown__content__diet');
        const icon = document.querySelector('.fa-caret-down');

        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none';
            icon.classList.remove('rotate'); 
        }
    }
}

//2й выпадющий список
function toggleDropdownRole() {
    const dropdownContent = document.querySelector('.dropdown__content__role');
    const icon = document.querySelector('.fa-caret-down'); 

    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
        icon.classList.remove('rotate'); 
    } else {
        dropdownContent.style.display = 'block';
        icon.classList.add('rotate'); 
    }
}

function selectItemRole(item) {
    document.getElementById('RoleInput').value = item; 
    document.querySelector('.dropdown__content__role').style.display = 'none'; 
    document.querySelector('.fa-caret-down').classList.remove('rotate'); 
}

window.onclick = function(event) {
    if (!event.target.matches('#RoleInput') && !event.target.matches('.icon')) {
        const dropdownContent = document.querySelector('.dropdown__content__role');
        const icon = document.querySelector('.fa-caret-down');

        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none';
            icon.classList.remove('rotate'); 
        }
    }
}









