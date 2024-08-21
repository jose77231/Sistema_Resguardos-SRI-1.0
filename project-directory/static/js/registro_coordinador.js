document.getElementById('registro-coordinador-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        correo: document.getElementById('correo').value,
        telefono: document.getElementById('telefono').value,
        password: document.getElementById('password').value
    };

    fetch('http://192.168.0.241:5000/registro/coordinador', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/templates/coordinadores.html';
        } else {
            return response.json().then(data => {
                document.getElementById('error-message').innerText = data.message;
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
