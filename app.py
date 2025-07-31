# app.py

from flask import Flask, jsonify, request
from models import db, Tarea
import os

app = Flask(__name__)

# Configuración de la base de datos
# SQLALCHEMY_DATABASE_URI: URL de conexión a la base de datos
# 'sqlite:///tareas.db': crea un archivo tareas.db en el directorio actual
# SQLite es perfecto para aprender porque no necesita servidor separado
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'

# SQLALCHEMY_TRACK_MODIFICATIONS: desactiva el tracking de modificaciones
# Esto mejora el rendimiento y evita warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con nuestra aplicación Flask
# Esto conecta SQLAlchemy con Flask
db.init_app(app)

def validar_tarea(datos):
    """
    Función de validación - verifica que los datos sean correctos
    """
    if not datos:
        return False, "No se enviaron datos"
    
    if 'titulo' not in datos:
        return False, "El campo 'titulo' es requerido"
    
    if 'descripcion' not in datos:
        return False, "El campo 'descripcion' es requerido"
    
    if not isinstance(datos['titulo'], str):
        return False, "El campo 'titulo' debe ser texto"
    
    if not isinstance(datos['descripcion'], str):
        return False, "El campo 'descripcion' debe ser texto"
    
    if len(datos['titulo']) < 1:
        return False, "El título no puede estar vacío"
    
    if len(datos['titulo']) > 100:
        return False, "El título no puede tener más de 100 caracteres"
    
    if len(datos['descripcion']) < 1:
        return False, "La descripción no puede estar vacía"
    
    return True, "Datos válidos"

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    """
    Obtener todas las tareas de la base de datos
    """
    # Tarea.query.all(): consulta SQL equivalente a "SELECT * FROM tareas"
    # Esto trae todas las tareas de la base de datos
    tareas = Tarea.query.all()
    
    # Convertimos cada tarea a diccionario usando el método to_dict()
    # jsonify necesita diccionarios para convertirlos a JSON
    return jsonify([tarea.to_dict() for tarea in tareas])

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    """
    Crear una nueva tarea en la base de datos
    """
    # Validar los datos de entrada
    es_valido, mensaje = validar_tarea(request.json)
    if not es_valido:
        return jsonify({"error": mensaje}), 400
    
    # Crear una nueva instancia de Tarea
    # Los campos id y fecha_creacion se llenan automáticamente
    nueva_tarea = Tarea(
        titulo=request.json['titulo'],
        descripcion=request.json['descripcion'],
        completada=request.json.get('completada', False)  # Por defecto False
    )
    
    # Agregar la tarea a la base de datos
    # db.session: maneja la sesión de la base de datos
    # add(): agrega el objeto para ser guardado
    # commit(): ejecuta la operación en la base de datos
    db.session.add(nueva_tarea)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea agregada", 
        "tarea": nueva_tarea.to_dict()
    }), 201

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    """
    Actualizar una tarea existente en la base de datos
    """
    # Validar los datos de entrada
    es_valido, mensaje = validar_tarea(request.json)
    if not es_valido:
        return jsonify({"error": mensaje}), 400
    
    # Buscar la tarea por ID
    # Tarea.query.get(tarea_id): consulta SQL equivalente a "SELECT * FROM tareas WHERE id = tarea_id"
    tarea = Tarea.query.get(tarea_id)
    
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    # Actualizar los campos de la tarea
    tarea.titulo = request.json['titulo']
    tarea.descripcion = request.json['descripcion']
    tarea.completada = request.json.get('completada', tarea.completada)
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea actualizada", 
        "tarea": tarea.to_dict()
    }), 200

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """
    Eliminar una tarea de la base de datos
    """
    # Buscar la tarea por ID
    tarea = Tarea.query.get(tarea_id)
    
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    # Guardar una copia de la tarea antes de eliminarla (para la respuesta)
    tarea_eliminada = tarea.to_dict()
    
    # Eliminar la tarea de la base de datos
    # db.session.delete(): marca el objeto para ser eliminado
    # db.session.commit(): ejecuta la operación
    db.session.delete(tarea)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea eliminada", 
        "tarea": tarea_eliminada
    }), 200

# Crear las tablas de la base de datos
# Esto debe ejecutarse una sola vez al iniciar la aplicación
def crear_tablas():
    """
    Crear todas las tablas definidas en los modelos
    """
    with app.app_context():
        # db.create_all(): crea todas las tablas que no existen
        # Es seguro ejecutarlo múltiples veces (no recrea tablas existentes)
        db.create_all()
        print("✅ Base de datos creada/verificada correctamente")

if __name__ == '__main__':
    # Crear las tablas antes de iniciar el servidor
    crear_tablas()
    
    # Iniciar el servidor Flask
    app.run(debug=True, host="0.0.0.0")