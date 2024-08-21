from flask import Blueprint, request, jsonify, send_file
from app.models import db, Alumno, Resguardante, Sistema, RecursosMateriales, Coordinador, AsignacionBien, BajaBien, Bien, EstructuraOrganica, Mantenimiento, InventarioFisico, Usuario
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import secrets
import base64
import qrcode
import os
import io
import xlsxwriter

main = Blueprint('main', __name__)

# Helper functions for generating and clearing tokens
def generate_reset_token(user):
    user.token_recuperacion = secrets.token_urlsafe(16)
    user.token_expira = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

def clear_reset_token(user):
    user.token_recuperacion = None
    user.token_expira = None
    db.session.commit()

def corregir_padding_base64(data):
    """Corrige el padding de una cadena base64 si es necesario."""
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

# Rutas para Alumno
@main.route('/alumnos', methods=['GET', 'POST'])
def manage_alumnos():
    if request.method == 'GET':
        alumnos = Alumno.query.all()
        return jsonify([alumno.to_dict() for alumno in alumnos])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_alumno = Alumno(**data)
        db.session.add(nuevo_alumno)
        db.session.commit()
        return jsonify(nuevo_alumno.to_dict()), 201

@main.route('/alumnos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(alumno.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(alumno, key, value)
        db.session.commit()
        return jsonify(alumno.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(alumno)
        db.session.commit()
        return '', 204

# Rutas para AsignacionBien
@main.route('/asignacion_bienes', methods=['GET', 'POST'])
def manage_asignacion_bienes():
    if request.method == 'GET':
        asignaciones = AsignacionBien.query.all()
        return jsonify([asignacion.to_dict() for asignacion in asignaciones])
    elif request.method == 'POST':
        data = request.get_json()
        nueva_asignacion = AsignacionBien(**data)
        db.session.add(nueva_asignacion)
        db.session.commit()
        return jsonify(nueva_asignacion.to_dict()), 201

@main.route('/asignacion_bienes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_asignacion_bien(id):
    asignacion = AsignacionBien.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(asignacion.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(asignacion, key, value)
        db.session.commit()
        return jsonify(asignacion.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(asignacion)
        db.session.commit()
        return '', 204

# Rutas para BajaBien
@main.route('/bajas_bienes', methods=['GET', 'POST'])
def manage_bajas_bienes():
    if request.method == 'GET':
        bajas = BajaBien.query.all()
        return jsonify([baja.to_dict() for baja in bajas])
    elif request.method == 'POST':
        data = request.get_json()
        nueva_baja = BajaBien(**data)
        db.session.add(nueva_baja)
        db.session.commit()
        return jsonify(nueva_baja.to_dict()), 201

@main.route('/bajas_bienes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_baja_bien(id):
    baja = BajaBien.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(baja.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(baja, key, value)
        db.session.commit()
        return jsonify(baja.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(baja)
        db.session.commit()
        return '', 204

# Rutas para Bienes
@main.route('/bienes', methods=['GET', 'POST'])
def manage_bienes():
    if request.method == 'GET':
        bienes = Bien.query.all()
        return jsonify([bien.to_dict() for bien in bienes])
    elif request.method == 'POST':
        data = request.form.to_dict()

        # Manejo de la imagen
        imagen_file = request.files.get('imagen')
        if imagen_file:
            imagen_binario = imagen_file.read()
        else:
            imagen_binario = None

        # Verificar o generar código QR
        codigo_qr = data.get('codigo_qr')
        if not codigo_qr:
            # Si no se proporciona código QR, generar uno
            codigo_qr = f"QR-{data.get('numero_inventario')}-{data.get('numero_serie')}"
            img = qrcode.make(codigo_qr)
            img.save(f"{codigo_qr}.png")  # Puedes guardar la imagen del QR si es necesario

        nuevo_bien = Bien(
            numero_serie=data.get('numero_serie'),
            nombre=data.get('nombre'),
            numero_inventario=data.get('numero_inventario'),
            descripcion=data.get('descripcion'),
            observaciones=data.get('observaciones'),
            fecha=datetime.strptime(data.get('fecha'), '%Y-%m-%d'),
            area=data.get('area'),
            categoria=data.get('categoria'),
            imagen=imagen_binario,
            codigo_qr=codigo_qr,
            estado=data.get('estado', 'activo'),
            asignado_a=data.get('asignado_a')  # Asegúrate de pasar el ID del usuario asignado
        )
        db.session.add(nuevo_bien)
        db.session.commit()
        return jsonify(nuevo_bien.to_dict()), 201

@main.route('/bienes/<int:id>', methods=['PUT'])
def actualizar_bien(id):
    bien = Bien.query.get_or_404(id)

    # Accediendo a los datos enviados en el formulario
    bien.nombre = request.form.get('nombre', bien.nombre)
    bien.numero_inventario = request.form.get('numero_inventario', bien.numero_inventario)
    bien.numero_serie = request.form.get('numero_serie', bien.numero_serie)
    bien.descripcion = request.form.get('descripcion', bien.descripcion)
    bien.observaciones = request.form.get('observaciones', bien.observaciones)
    bien.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d') if request.form.get('fecha') else bien.fecha
    bien.area = request.form.get('area', bien.area)
    bien.categoria = request.form.get('categoria', bien.categoria)
    bien.estado = request.form.get('estado', bien.estado)
    bien.asignado_a = request.form.get('asignado_a', bien.asignado_a)  # ID del asignado

    # Si se sube una nueva imagen
    if 'imagen' in request.files:
        bien.imagen = request.files['imagen'].read()

    db.session.commit()
    return jsonify(bien.to_dict()), 200

@main.route('/bienes/<int:id>', methods=['GET'])
def obtener_bien(id):
    bien = Bien.query.get_or_404(id)
    coordinadores = Coordinador.query.all()
    sistemas = Sistema.query.all()

    response = {
        'bien': bien.to_dict(),
        'coordinadores': [c.to_dict() for c in coordinadores],
        'sistemas': [s.to_dict() for s in sistemas]
    }

    return jsonify(response), 200

# Rutas para Coordinador
@main.route('/coordinadores', methods=['GET', 'POST'])
def manage_coordinadores():
    if request.method == 'GET':
        coordinadores = Coordinador.query.all()
        return jsonify([coordinador.to_dict() for coordinador in coordinadores])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_coordinador = Coordinador(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            correo=data.get('correo'),
            telefono=data.get('telefono'),
            password=data.get('password'),
            estado=data.get('estado', 'activo'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(nuevo_coordinador)
        db.session.commit()
        return jsonify(nuevo_coordinador.to_dict()), 201

@main.route('/coordinadores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_coordinador(id):
    coordinador = Coordinador.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(coordinador.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        coordinador.nombre = data.get('nombre', coordinador.nombre)
        coordinador.apellido = data.get('apellido', coordinador.apellido)
        coordinador.correo = data.get('correo', coordinador.correo)
        coordinador.telefono = data.get('telefono', coordinador.telefono)
        coordinador.password = data.get('password', coordinador.password)
        coordinador.estado = data.get('estado', coordinador.estado)
        coordinador.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(coordinador.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(coordinador)
        db.session.commit()
        return '', 204

# Rutas para EstructuraOrganica
@main.route('/estructura_organica', methods=['GET', 'POST'])
def manage_estructura_organica():
    if request.method == 'GET':
        estructuras = EstructuraOrganica.query.all()
        return jsonify([estructura.to_dict() for estructura in estructuras])
    elif request.method == 'POST':
        data = request.get_json()
        nueva_estructura = EstructuraOrganica(
            Nivel=data.get('nivel'),
            Nombre=data.get('nombre'),
            Area=data.get('area'),
            cargo=data.get('cargo')
        )
        db.session.add(nueva_estructura)
        db.session.commit()
        return jsonify(nueva_estructura.to_dict()), 201

@main.route('/estructura_organica/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_estructura_organica_item(id):
    estructura = EstructuraOrganica.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(estructura.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(estructura, key, value)
        db.session.commit()
        return jsonify(estructura.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(estructura)
        db.session.commit()
        return '', 204

# Rutas para Mantenimiento
@main.route('/mantenimiento', methods=['GET', 'POST'])
def manage_mantenimiento():
    if request.method == 'GET':
        mantenimientos = Mantenimiento.query.all()
        return jsonify([mantenimiento.to_dict() for mantenimiento in mantenimientos])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_mantenimiento = Mantenimiento(**data)
        db.session.add(nuevo_mantenimiento)
        db.session.commit()
        return jsonify(nuevo_mantenimiento.to_dict()), 201

@main.route('/mantenimiento/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_mantenimiento_item(id):
    mantenimiento = Mantenimiento.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(mantenimiento.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(mantenimiento, key, value)
        db.session.commit()
        return jsonify(mantenimiento.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(mantenimiento)
        db.session.commit()
        return '', 204

# Rutas para Resguardante
@main.route('/resguardantes', methods=['GET', 'POST'])
def manage_resguardantes():
    if request.method == 'GET':
        resguardantes = Resguardante.query.all()
        return jsonify([resguardante.to_dict() for resguardante in resguardantes])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_resguardante = Resguardante(**data)
        db.session.add(nuevo_resguardante)
        db.session.commit()
        return jsonify(nuevo_resguardante.to_dict()), 201

@main.route('/resguardantes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_resguardante(id):
    resguardante = Resguardante.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(resguardante.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(resguardante, key, value)
        db.session.commit()
        return jsonify(resguardante.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(resguardante)
        db.session.commit()
        return '', 204

# Rutas para Sistema
@main.route('/sistemas', methods=['GET', 'POST'])
def manage_sistemas():
    if request.method == 'GET':
        sistemas = Sistema.query.all()
        return jsonify([sistema.to_dict() for sistema in sistemas])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_sistema = Sistema(**data)
        db.session.add(nuevo_sistema)
        db.session.commit()
        return jsonify(nuevo_sistema.to_dict()), 201

@main.route('/sistemas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_sistema(id):
    sistema = Sistema.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(sistema.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(sistema, key, value)
        db.session.commit()
        return jsonify(sistema.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(sistema)
        db.session.commit()
        return '', 204

# Rutas para RecursosMateriales
@main.route('/recursos_materiales', methods=['GET', 'POST'])
def manage_recursos_materiales():
    if request.method == 'GET':
        recursos = RecursosMateriales.query.all()
        return jsonify([recurso.to_dict() for recurso in recursos])
    elif request.method == 'POST':
        data = request.get_json()
        nuevo_recurso = RecursosMateriales(**data)
        db.session.add(nuevo_recurso)
        db.session.commit()
        return jsonify(nuevo_recurso.to_dict()), 201

@main.route('/recursos_materiales/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_recurso_material(id):
    recurso = RecursosMateriales.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(recurso.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(recurso, key, value)
        db.session.commit()
        return jsonify(recurso.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(recurso)
        db.session.commit()
        return '', 204

# Ruta para login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    user = None
    role = None

    # Check in each user type table
    user = Alumno.query.filter_by(correo=correo).first()
    if user and user.password == password:
        role = 'alumno'
    else:
        user = Resguardante.query.filter_by(correo=correo).first()
        if user and user.password == password:
            role = 'resguardante'
        else:
            user = Sistema.query.filter_by(correo=correo).first()
            if user and user.password == password:
                role = 'sistema'
            else:
                user = RecursosMateriales.query.filter_by(correo=correo).first()
                if user and user.password == password:
                    role = 'administrador'

    if user:
        return jsonify({'success': True, 'role': role})
    else:
        return jsonify({'success': False, 'message': 'Correo o contraseña incorrectos'}), 401

# Ruta para recuperar contraseña (enviar token)
@main.route('/recuperar_contrasena', methods=['POST'])
def recuperar_contrasena():
    data = request.get_json()
    correo = data.get('correo')

    user = (Alumno.query.filter_by(correo=correo).first() or
            Resguardante.query.filter_by(correo=correo).first() or
            Sistema.query.filter_by(correo=correo).first() or
            RecursosMateriales.query.filter_by(correo=correo).first() or
            Coordinador.query.filter_by(correo=correo).first())

    if not user:
        return jsonify({'success': False, 'message': 'Correo no encontrado'}), 404

    # Generate a reset token
    generate_reset_token(user)

    # Send email with token
    msg = MIMEText(f"Usa este código para recuperar tu cuenta: {user.token_recuperacion}")
    msg['Subject'] = 'Recuperación de contraseña'
    msg['From'] = 'suporteadc61@gmail.com'
    msg['To'] = correo

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('sonic77231@gmail.com', 'tcwf hibz lrkc nhmt')
            server.sendmail('sonic77231@gmail.com', [correo], msg.as_string())
        return jsonify({'success': True, 'message': 'Correo enviado correctamente'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error enviando correo: {str(e)}'}), 500

# Ruta para verificar código de recuperación
@main.route('/verificar_codigo', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    correo = data.get('correo')
    codigo = data.get('codigo')

    # Intenta encontrar el usuario en cualquiera de las tablas
    user = (Alumno.query.filter_by(correo=correo, token_recuperacion=codigo).first() or
            Resguardante.query.filter_by(correo=correo, token_recuperacion=codigo).first() or
            Sistema.query.filter_by(correo=correo, token_recuperacion=codigo).first() or
            RecursosMateriales.query.filter_by(correo=correo, token_recuperacion=codigo).first() or
            Coordinador.query.filter_by(correo=correo, token_recuperacion=codigo).first())

    # Verifica si no se encontró el usuario o si el token ha expirado
    if not user:
        return jsonify({'success': False, 'message': 'Usuario no encontrado o código incorrecto'}), 400

    # Asegúrate de que el token no haya expirado
    if user.token_expira < datetime.utcnow():
        return jsonify({'success': False, 'message': 'Código expirado'}), 400

    # Si todo es correcto
    return jsonify({'success': True})

# Ruta para cambiar la contraseña
@main.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    data = request.get_json()
    correo = data.get('correo')
    nueva_contrasena = data.get('nueva_contrasena')

    user = (Alumno.query.filter_by(correo=correo).first() or
            Resguardante.query.filter_by(correo=correo).first() or
            Sistema.query.filter_by(correo=correo).first() or
            RecursosMateriales.query.filter_by(correo=correo).first() or
            Coordinador.query.filter_by(correo=correo).first())

    if not user:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    # Update the password
    user.password = nueva_contrasena
    clear_reset_token(user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Contraseña actualizada con éxito'})

# Rutas para Inventario Fisico
@main.route('/inventario-fisico', methods=['GET'])
def get_inventario_fisico():
    try:
        inventario_fisico = InventarioFisico.query.all()
        return jsonify([bien.to_dict() for bien in inventario_fisico])
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")
        return jsonify({'error': 'Error retrieving data'}), 500

@main.route('/inventario-fisico/<int:id>', methods=['GET'])
def get_inventario_fisico_by_id(id):
    try:
        bien = InventarioFisico.query.get_or_404(id)
        return jsonify(bien.to_dict())
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")
        return jsonify({'error': 'Error retrieving data'}), 500

# Ruta para generar y descargar el reporte
@main.route('/reporte_usuarios', methods=['GET'])
def reporte_usuarios():
    try:
        # Crear un buffer de bytes en memoria
        output = io.BytesIO()

        # Crear un archivo Excel en memoria
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Agregar datos al Excel (puedes modificarlo para tus necesidades)
        worksheet.write('A1', 'Nombre')
        worksheet.write('B1', 'Apellido')
        worksheet.write('C1', 'Teléfono')
        worksheet.write('D1', 'Correo')

        # Simula los datos de usuarios para la demostración
        usuarios = [
            {"nombre": "José", "apellido": "Manzo", "telefono": "9831076765", "correo": "hose.jm5@gmail.com"},
            # Añade más datos según sea necesario
        ]

        row = 1
        for usuario in usuarios:
            worksheet.write(row, 0, usuario['nombre'])
            worksheet.write(row, 1, usuario['apellido'])
            worksheet.write(row, 2, usuario['telefono'])
            worksheet.write(row, 3, usuario['correo'])
            row += 1

        # Cerrar el workbook
        workbook.close()

        # Mover el puntero al inicio del archivo
        output.seek(0)

        # Enviar el archivo Excel al cliente
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, download_name='reporte_usuarios.xlsx')

    except Exception as e:
        return jsonify({"error": str(e)})

# Ruta para obtener y crear usuarios
@main.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@main.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.form.to_dict()

    imagen_file = request.files.get('imagen')
    if imagen_file:
        imagen_binario = imagen_file.read()
    else:
        imagen_binario = None

    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        genero=data.get('genero'),
        correo=data.get('correo'),
        telefono=data.get('telefono'),
        bienes_asignados=data.get('bienes_asignados', 0),
        imagen=imagen_binario
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201
@main.route('/estructura_organica', methods=['POST'])
def add_estructura_organica():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos no proporcionados o JSON malformado"}), 400

        nueva_estructura = EstructuraOrganica(
            nivel=data.get('nivel'),
            nombre=data.get('nombre'),
            cargo=data.get('cargo'),
            area=data.get('area')
        )
        
        db.session.add(nueva_estructura)
        db.session.commit()

        return jsonify({"message": "Estructura orgánica guardada correctamente"}), 201
    
    except Exception as e:
        print("Error al guardar estructura orgánica:", str(e))  # Depuración
        return jsonify({"error": str(e)}), 500


@main.route('/estructura_organica', methods=['GET'])
def get_estructura_organica():
    estructuras = EstructuraOrganica.query.all()
    result = [{
        "id": estructura.id,
        "nivel": estructura.nivel,
        "nombre": estructura.nombre,
        "cargo": estructura.cargo,
        "area": estructura.area
    } for estructura in estructuras]
    
    return jsonify(result), 200

@main.route('/estructura_organica/<int:id>', methods=['DELETE'])
def eliminar_estructura_organica(id):
    estructura = EstructuraOrganica.query.get_or_404(id)
    db.session.delete(estructura)
    db.session.commit()
    return '', 204
