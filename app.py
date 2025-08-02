# app.py

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Tarea, Usuario
import os
from datetime import timedelta

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de JWT
# SECRET_KEY: clave secreta para firmar los tokens (en producción debe ser muy segura)
app.config['JWT_SECRET_KEY'] = 'tu-clave-secreta-super-segura'
# JWT_ACCESS_TOKEN_EXPIRES: tiempo de expiración del token (7 días)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)

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

def validar_usuario(datos):
    """
    Función de validación para datos de usuario
    """
    if not datos:
        return False, "No se enviaron datos"
    
    if 'username' not in datos:
        return False, "El campo 'username' es requerido"
    
    if 'email' not in datos:
        return False, "El campo 'email' es requerido"
    
    if 'password' not in datos:
        return False, "El campo 'password' es requerido"
    
    if not isinstance(datos['username'], str) or len(datos['username']) < 3:
        return False, "El username debe tener al menos 3 caracteres"
    
    if not isinstance(datos['email'], str) or '@' not in datos['email']:
        return False, "El email debe ser válido"
    
    if not isinstance(datos['password'], str) or len(datos['password']) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    return True, "Datos válidos"

@app.route('/registro', methods=['POST'])
def registro():
    """
    Registrar un nuevo usuario
    """
    # Validar los datos de entrada
    es_valido, mensaje = validar_usuario(request.json)
    if not es_valido:
        return jsonify({"error": mensaje}), 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(username=request.json['username']).first():
        return jsonify({"error": "El username ya está en uso"}), 400
    
    if Usuario.query.filter_by(email=request.json['email']).first():
        return jsonify({"error": "El email ya está registrado"}), 400
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        username=request.json['username'],
        email=request.json['email']
    )
    nuevo_usuario.set_password(request.json['password'])
    
    # Guardar en la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Usuario registrado exitosamente",
        "usuario": nuevo_usuario.to_dict()
    }), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión de usuario
    """
    if not request.json:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username y password son requeridos"}), 400
    
    # Buscar usuario por username
    usuario = Usuario.query.filter_by(username=username).first()
    
    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Username o password incorrectos"}), 401
    
    # Crear token de acceso
    access_token = create_access_token(identity=str(usuario.id))
    
    return jsonify({
        "mensaje": "Login exitoso",
        "access_token": access_token,
        "usuario": usuario.to_dict()
    }), 200

@app.route('/tareas', methods=['GET'])
@jwt_required()
def obtener_tareas():
    """
    Obtener todas las tareas del usuario autenticado
    """
    # get_jwt_identity(): obtiene el ID del usuario del token
    usuario_id = int(get_jwt_identity())
    
    # Buscar tareas del usuario específico
    tareas = Tarea.query.filter_by(usuario_id=usuario_id).all()
    
    return jsonify([tarea.to_dict() for tarea in tareas])

@app.route('/tareas', methods=['POST'])
@jwt_required()
def agregar_tarea():
    """
    Crear una nueva tarea para el usuario autenticado
    """
    # Validar los datos de entrada
    es_valido, mensaje = validar_tarea(request.json)
    if not es_valido:
        return jsonify({"error": mensaje}), 400
    
    # Obtener ID del usuario autenticado
    usuario_id = get_jwt_identity()
    
    # Crear nueva tarea
    nueva_tarea = Tarea(
        titulo=request.json['titulo'],
        descripcion=request.json['descripcion'],
        completada=request.json.get('completada', False),
        usuario_id=usuario_id
    )
    
    # Guardar en la base de datos
    db.session.add(nueva_tarea)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea agregada",
        "tarea": nueva_tarea.to_dict()
    }), 201

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
@jwt_required()
def actualizar_tarea(tarea_id):
    """
    Actualizar una tarea del usuario autenticado
    """
    # Validar los datos de entrada
    es_valido, mensaje = validar_tarea(request.json)
    if not es_valido:
        return jsonify({"error": mensaje}), 400
    
    # Obtener ID del usuario autenticado
    usuario_id = get_jwt_identity()
    
    # Buscar la tarea del usuario específico
    tarea = Tarea.query.filter_by(id=tarea_id, usuario_id=usuario_id).first()
    
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    # Actualizar campos
    tarea.titulo = request.json['titulo']
    tarea.descripcion = request.json['descripcion']
    tarea.completada = request.json.get('completada', tarea.completada)
    
    # Guardar cambios
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea actualizada",
        "tarea": tarea.to_dict()
    }), 200

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
@jwt_required()
def eliminar_tarea(tarea_id):
    """
    Eliminar una tarea del usuario autenticado
    """
    # Obtener ID del usuario autenticado
    usuario_id = get_jwt_identity()
    
    # Buscar la tarea del usuario específico
    tarea = Tarea.query.filter_by(id=tarea_id, usuario_id=usuario_id).first()
    
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    # Guardar copia antes de eliminar
    tarea_eliminada = tarea.to_dict()
    
    # Eliminar tarea
    db.session.delete(tarea)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Tarea eliminada",
        "tarea": tarea_eliminada
    }), 200

# ===========================================
# MANEJO DE ERRORES
# ===========================================

@app.errorhandler(404)
def not_found(error):
    """
    Maneja errores 404 - Recurso no encontrado
    """
    return jsonify({
        "error": "Recurso no encontrado",
        "mensaje": "La URL que buscas no existe"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """
    Maneja errores 405 - Método no permitido
    """
    return jsonify({
        "error": "Método no permitido",
        "mensaje": "El método HTTP que usaste no está permitido para esta URL"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """
    Maneja errores 500 - Error interno del servidor
    """
    return jsonify({
        "error": "Error interno del servidor",
        "mensaje": "Algo salió mal en el servidor. Inténtalo de nuevo más tarde."
    }), 500

# Crear las tablas de la base de datos
def crear_tablas():
    """
    Crear todas las tablas definidas en los modelos
    """
    with app.app_context():
        db.create_all()
        print("✅ Base de datos creada/verificada correctamente")

if __name__ == '__main__':
    # Crear las tablas antes de iniciar el servidor
    crear_tablas()
    
    # Iniciar el servidor Flask
    app.run(debug=True, host="0.0.0.0")