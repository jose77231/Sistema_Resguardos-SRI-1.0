document.getElementById('recovery-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const correo = document.getElementById('correo').value;

    fetch('http://192.168.0.241:5000/recuperar_contrasena', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo: correo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = 'espera.html';
        } else {
            document.getElementById('error-message').textContent = 'Error enviando el correo de recuperación.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'Error en el servidor.';
    });
});
