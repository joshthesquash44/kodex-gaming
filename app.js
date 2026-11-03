const modal = document.getElementById('gameModal');
const frame = document.getElementById('gameFrame');
const openButtons = document.querySelectorAll('[data-open-game]');
const closeButton = document.getElementById('closeGame');

function openArcade() {
  frame.src = 'games/arcade/index.html';
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}
function closeArcade() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  frame.src = 'about:blank';
  document.body.style.overflow = '';
}
openButtons.forEach(button => button.addEventListener('click', openArcade));
closeButton.addEventListener('click', closeArcade);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && modal.classList.contains('open')) closeArcade();
});
