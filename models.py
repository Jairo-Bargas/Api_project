# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Creamos una instancia de SQLAlchemy
# Esto nos permite trabajar con bases de datos de forma más fácil
db = SQLAlchemy()

class Tarea(db.Model):
    """
    Modelo de Tarea - Define la estructura de datos en la base de datos
    
    Cada campo representa una columna en la tabla 'tareas'
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'tareas'
    
    
    #LA ESTRUCTURA DE SQLALCHEMY ES EN ESTE CASO: DB.COLUM(TIPO DE DATO, OPCIONES..)
    
    
    # Campo id: clave primaria, se auto-incrementa
    # Integer: tipo de dato entero
    # primary_key=True: indica que es la clave principal
    # autoincrement=True: se incrementa automáticamente
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Campo titulo: texto obligatorio, máximo 100 caracteres
    # String(100): tipo de dato texto con máximo 100 caracteres
    # nullable=False: no puede estar vacío
    titulo = db.Column(db.String(100), nullable=False)
    
    # Campo descripcion: texto obligatorio
    # Text: tipo de dato texto sin límite de caracteres
    # nullable=False: no puede estar vacío
    descripcion = db.Column(db.Text, nullable=False)
    
    # Campo completada: booleano, por defecto False
    # Boolean: tipo de dato verdadero/falso
    # default=False: valor por defecto es False
    completada = db.Column(db.Boolean, default=False)
    
    # Campo fecha_creacion: fecha y hora de creación
    # DateTime: tipo de dato fecha y hora
    # default=datetime.utcnow: valor por defecto es la fecha/hora actual
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """
        Convierte el objeto Tarea a un diccionario (para JSON)
        Esto es útil para enviar datos al frontend
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def __repr__(self):
        """
        Representación en texto del objeto (útil para debugging)
        """
        return f'<Tarea {self.id}: {self.titulo}>' 