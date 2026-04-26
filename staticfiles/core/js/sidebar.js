const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
const sidebarClose = document.getElementById('sidebarClose');
const sidebarOverlay = document.getElementById('sidebarOverlay');

function openSidebar() {
    sidebar.classList.add('open');
    sidebarOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Открытие по кнопке меню
if (menuToggle) {
    menuToggle.addEventListener('click', openSidebar);
}

// Закрытие по крестику
if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
}

// Закрытие по оверлею
if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
}

// Закрытие по клавише ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
        closeSidebar();
    }
});