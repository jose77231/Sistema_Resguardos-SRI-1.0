let countdown = 60;
const countdownElement = document.getElementById('countdown');
const resendButton = document.getElementById('resend-code');
const enterCodeButton = document.getElementById('enter-code');

const countdownInterval = setInterval(() => {
    countdown--;
    countdownElement.textContent = countdown;
    if (countdown <= 0) {
        clearInterval(countdownInterval);
        resendButton.disabled = false;
    }
}, 1000);

resendButton.addEventListener('click', function() {
    fetch('http://192.168.0.241:5000/recuperar_contrasena', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo: localStorage.getItem('correo') })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            countdown = 60;
            resendButton.disabled = true;
            setInterval(countdownInterval, 1000);
        }
    })
    .catch(error => console.error('Error:', error));
});

enterCodeButton.addEventListener('click', function() {
    window.location.href = 'codigo.html';
});
