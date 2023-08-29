const heroElement = document.querySelector('.hero-img');
const fadeClasses = ['fade-1', 'fade-2', 'fade-3'];
let currentFadeIndex = 0;

function changeFade() {
  heroElement.classList.remove(...fadeClasses);
  currentFadeIndex = (currentFadeIndex + 1) % fadeClasses.length;
  heroElement.classList.add(fadeClasses[currentFadeIndex]);
}

// Call the changeFade function periodically
setInterval(changeFade, 3000); // Transition every 30 seconds
