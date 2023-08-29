const loginElement = document.querySelector('.login-img');
const dotClasses = ['.dot1', '.dot2', '.dot3'];
const pickerElement = 'pick1';
const fadeClasses = ['fade1', 'fade2', 'fade3'];
let currentFadeIndex = 0;

function changeFade() {
  
  
  loginElement.classList.remove(...fadeClasses);
  
  currentFadeIndex = (currentFadeIndex + 1) % fadeClasses.length;
  
  loginElement.classList.add(fadeClasses[currentFadeIndex]);

}


// Call the changeFade function periodically
setInterval(changeFade, 3000); // Transition every 3 seconds

