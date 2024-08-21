document.getElementById('password-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (newPassword !== confirmPassword) {
        document.getElementById('error-message').textContent = 'Las contraseñas no coinciden.';
        return;
    }

    fetch('http://192.168.0.241:5000/cambiar_contrasena', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo: localStorage.getItem('correo'), nueva_contrasena: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Contraseña cambiada con éxito.');
            window.location.href = 'login.html';
        } else {
            document.getElementById('error-message').textContent = 'Error al cambiar la contraseña.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'Error en el servidor.';
    });
});
