document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const correo = document.getElementById('correo').value;
    const password = document.getElementById('password').value;

    fetch('http://192.168.0.241:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.role === 'administrador') {
                window.location.href = 'templates/administrador.html';
            } else if (data.role === 'resguardante') {
                window.location.href = 'templates/resguardantes.html';
            } else if (data.role === 'sistema') {
                window.location.href = 'templates/sistemas.html';
            } else if (data.role === 'alumno') {
                window.location.href = 'templates/alumnos.html';
            }
        } else {
            document.getElementById('error-message').textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'Error en el servidor.';
    });
});
document.getElementById('forgot-password').addEventListener('click', function() {
    window.location.href = 'recuperar_correo.html';
});

