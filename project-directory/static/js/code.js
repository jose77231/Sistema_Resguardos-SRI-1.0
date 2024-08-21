document.getElementById('code-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const codigo = document.getElementById('codigo').value;
    const correo = localStorage.getItem('correo');

    console.log('Código:', codigo);
    console.log('Correo:', correo);

    fetch('http://192.168.0.241:5000/verificar_codigo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo: correo, codigo: codigo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = 'cambiar_contrasena.html';
        } else {
            document.getElementById('error-message').textContent = 'Código incorrecto.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'Error en el servidor.';
    });
});
