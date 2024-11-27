document.addEventListener('DOMContentLoaded', () => {
    const menuIcon = document.getElementById('menu-icon');
    const sideNav = document.getElementById('sideNav');
    const mainContent = document.querySelector('.main-content');

    menuIcon.addEventListener('click', () => {
        sideNav.classList.toggle('side-nav-active');
        mainContent.classList.toggle('main-content-active');
    });
});
