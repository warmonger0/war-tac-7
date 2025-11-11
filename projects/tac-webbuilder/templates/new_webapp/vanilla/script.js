// Simple counter example
let count = 0;
const button = document.getElementById('counterBtn');

button.addEventListener('click', () => {
    count++;
    button.textContent = `Click me: ${count}`;
});

console.log('Vanilla JavaScript app loaded!');
