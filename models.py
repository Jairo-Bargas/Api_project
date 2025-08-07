# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Creamos una instancia de SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    """
    Modelo de Usuario - Define la estructura de datos para usuarios
    
    Cada usuario puede tener múltiples tareas (relación uno a muchos)
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'
    
    # Campo id: clave primaria, se auto-incrementa
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Campo username: nombre de usuario único
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Campo email: email único
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Campo password_hash: contraseña encriptada
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Campo fecha_registro: fecha y hora de registro
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con tareas: un usuario puede tener muchas tareas
    # backref='usuario': permite acceder al usuario desde una tarea
    tareas = db.relationship('Tarea', backref='usuario', lazy=True, cascade='all, delete-orphan') #Lazy=true carga solo las tareas solo cuando se necesiten, backref deja que acceda a usuario desde tarea 
    
    def set_password(self, password):
        """
        Encripta la contraseña y la guarda en password_hash
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada es correcta
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario (sin la contraseña)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
        
        #¿Por qué es útil? Porque los objetos no son directamente "serializables". No podés mandar un objeto completo de SQLAlchemy como JSON. Pero sí podés mandar un diccionario. 
    
    def __repr__(self):
        """
        Representación en texto del objeto (útil para debugging)
        """
        return f'<Usuario {self.username}>'

class Tarea(db.Model):
    """
    Modelo de Tarea - Define la estructura de datos en la base de datos
    
    Cada campo representa una columna en la tabla 'tareas'
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'tareas'
    
    # Campo id: clave primaria, se auto-incrementa
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Campo titulo: texto obligatorio, máximo 100 caracteres
    titulo = db.Column(db.String(100), nullable=False)
    
    # Campo descripcion: texto obligatorio
    descripcion = db.Column(db.Text, nullable=False)
    
    # Campo completada: booleano, por defecto False
    completada = db.Column(db.Boolean, default=False)
    
    # Campo fecha_creacion: fecha y hora de creación
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campo usuario_id: clave foránea que conecta con la tabla usuarios
    # ForeignKey('usuarios.id'): referencia al campo id de la tabla usuarios
    # nullable=False: toda tarea debe pertenecer a un usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def to_dict(self):
        """
        Convierte el objeto Tarea a un diccionario (para JSON)
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id
        }
    
    def __repr__(self):
        """
        Representación en texto del objeto (útil para debugging)
        """
        return f'<Tarea {self.id}: {self.titulo}>'