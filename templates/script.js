const menuButton = document.querySelector('.menu-button');
const navLinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');

menuButton.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

links.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
  });
});
