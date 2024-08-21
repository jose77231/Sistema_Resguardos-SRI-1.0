from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import base64

db = SQLAlchemy()

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    matricula = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    password = db.Column(db.String(100), nullable=False)
    token_recuperacion = db.Column(db.String(100), nullable=True)
    token_expira = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password': self.password,
            'token_recuperacion': self.token_recuperacion,
            'token_expira': self.token_expira,
        }

class Resguardante(db.Model):
    __tablename__ = 'resguardantes'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    password = db.Column(db.String(100), nullable=False)
    token_recuperacion = db.Column(db.String(100), nullable=True)
    token_expira = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password': self.password,
            'token_recuperacion': self.token_recuperacion,
            'token_expira': self.token_expira,
        }

class Sistema(db.Model):
    __tablename__ = 'sistemas'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    password = db.Column(db.String(100), nullable=False)
    token_recuperacion = db.Column(db.String(100), nullable=True)
    token_expira = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password': self.password,
            'token_recuperacion': self.token_recuperacion,
            'token_expira': self.token_expira,
        }

class RecursosMateriales(db.Model):
    __tablename__ = 'recursos_materiales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    token_recuperacion = db.Column(db.String(100), nullable=True)
    token_expira = db.Column(db.DateTime, nullable=True)

    def generate_reset_token(self):
        self.token_recuperacion = str(uuid.uuid4())
        self.token_expira = datetime.utcnow() + timedelta(minutes=10)

    def clear_reset_token(self):
        self.token_recuperacion = None
        self.token_expira = None

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'password': self.password,
            'area': self.area,
            'token_recuperacion': self.token_recuperacion,
            'token_expira': self.token_expira,
        }

class Coordinador(db.Model):
    __tablename__ = 'coordinadores'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    password = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo', 'mantenimiento', 'baja'), nullable=False, default='activo')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'password': self.password,
            'estado': self.estado,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class AsignacionBien(db.Model):
    __tablename__ = 'asignacion_bienes'
    id = db.Column(db.BigInteger, primary_key=True)
    bien_id = db.Column(db.BigInteger, db.ForeignKey('bienes.id'), nullable=False)
    usuario_id = db.Column(db.BigInteger, nullable=False)
    tipo_usuario = db.Column(db.Enum('alumno', 'resguardante', 'sistema', 'coordinador'), nullable=False)
    fecha_asignacion = db.Column(db.Date, nullable=False)
    fecha_devolucion = db.Column(db.Date)
    estado = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'bien_id': self.bien_id,
            'usuario_id': self.usuario_id,
            'tipo_usuario': self.tipo_usuario,
            'fecha_asignacion': self.fecha_asignacion,
            'fecha_devolucion': self.fecha_devolucion,
            'estado': self.estado,
        }

class BajaBien(db.Model):
    __tablename__ = 'bajas_bienes'
    id = db.Column(db.BigInteger, primary_key=True)
    bien_id = db.Column(db.BigInteger, db.ForeignKey('bienes.id'), nullable=False)
    fecha_baja = db.Column(db.Date, nullable=False)
    motivo_baja = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'bien_id': self.bien_id,
            'fecha_baja': self.fecha_baja,
            'motivo_baja': self.motivo_baja,
        }

class Bien(db.Model):
    __tablename__ = 'bienes'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    numero_serie = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.Text, nullable=False)
    numero_inventario = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    observaciones = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    area = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=False)
    codigo_qr = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo', 'mantenimiento', 'baja'), default='activo', nullable=False)
    asignado_a = db.Column(db.BigInteger, nullable=True)  # Nuevo campo para la asignación

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'numero_serie': self.numero_serie,
            'nombre': self.nombre,
            'numero_inventario': self.numero_inventario,
            'descripcion': self.descripcion,
            'observaciones': self.observaciones,
            'fecha': self.fecha,
            'area': self.area,
            'categoria': self.categoria,
            'imagen': base64.b64encode(self.imagen).decode('utf-8') if self.imagen else None,
            'codigo_qr': self.codigo_qr,
            'estado': self.estado,
            'asignado_a': self.asignado_a,  # Incluir este campo en el diccionario
        }


class Mantenimiento(db.Model):
    __tablename__ = 'mantenimiento'
    id = db.Column(db.BigInteger, primary_key=True)
    bien_id = db.Column(db.BigInteger, db.ForeignKey('bienes.id'), nullable=False)
    fecha_mantenimiento = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'bien_id': self.bien_id,
            'fecha_mantenimiento': self.fecha_mantenimiento,
            'descripcion': self.descripcion,
        }

class InventarioFisico(db.Model):
    __tablename__ = 'inventario_fisico'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    numero_serie = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.Text, nullable=False)
    numero_inventario = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    observaciones = db.Column(db.String(500), nullable=False)
    area = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=False)
    codigo_qr = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo', 'mantenimiento', 'baja'), default='activo', nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'numero_serie': self.numero_serie,
            'nombre': self.nombre,
            'numero_inventario': self.numero_inventario,
            'estado_bien': self.estado,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'observaciones': self.observaciones,
            'imagen': f'data:image/png;base64,{base64.b64encode(self.imagen).decode("utf-8")}' if self.imagen else None
        }
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    bienes_asignados = db.Column(db.Integer, nullable=False, default=0)  # Número de bienes asignados
    imagen = db.Column(db.LargeBinary, nullable=True)  # Imagen en formato binario
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'genero': self.genero,
            'correo': self.correo,
            'telefono': self.telefono,
            'bienes_asignados': self.bienes_asignados,
            'imagen': base64.b64encode(self.imagen.encode('utf-8')).decode('utf-8') if isinstance(self.imagen, str) else base64.b64encode(self.imagen).decode('utf-8') if self.imagen else None,
        }
        
class EstructuraOrganica(db.Model):
    __tablename__ = 'estructura_organica'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nivel = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nivel': self.nivel,
            'nombre': self.nombre,
            'area': self.area,
            'cargo': self.cargo,
        }