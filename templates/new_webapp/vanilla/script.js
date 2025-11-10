// Simple counter application

let count = 0

const button = document.getElementById('counter-button')

if (button) {
  button.addEventListener('click', () => {
    count++
    button.textContent = `count is ${count}`
  })
}

// Add your custom JavaScript here
console.log('App loaded successfully!')
