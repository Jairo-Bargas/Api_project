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
    Función de validación mejorada para datos de usuario
    
    Esta función verifica que todos los campos requeridos estén presentes
    y que cumplan con las reglas de validación establecidas.
    
    Parámetros:
    - datos: diccionario con los datos del usuario (username, email, password)
    
    Retorna:
    - tupla (es_valido, mensaje): True si es válido, False si hay errores
    """
    # Verificar que se enviaron datos
    if not datos:
        return False, "No se enviaron datos"
    
    # Verificar que todos los campos requeridos estén presentes
    campos_requeridos = ['username', 'email', 'password']
    for campo in campos_requeridos:
        if campo not in datos:
            return False, f"El campo '{campo}' es requerido"
    
    # Validar username
    username = datos['username']
    if not isinstance(username, str):
        return False, "El username debe ser texto"
    
    if len(username) < 3:
        return False, "El username debe tener al menos 3 caracteres"
    
    if len(username) > 20:
        return False, "El username no puede tener más de 20 caracteres"
    
    # Verificar que username solo contenga letras, números y guiones bajos
    if not username.replace('_', '').isalnum():
        return False, "El username solo puede contener letras, números y guiones bajos (_)"
    
    # Validar email
    email = datos['email']
    if not isinstance(email, str):
        return False, "El email debe ser texto"
    
    # Validación básica de email (debe contener @ y un punto después del @)
    if '@' not in email or '.' not in email.split('@')[1]:
        return False, "El formato del email no es válido"
    
    # Validar password
    password = datos['password']
    if not isinstance(password, str):
        return False, "La contraseña debe ser texto"
    
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    if len(password) > 50:
        return False, "La contraseña no puede tener más de 50 caracteres"
    
    # Verificar que la contraseña tenga al menos una letra y un número
    tiene_letra = any(c.isalpha() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    
    if not tiene_letra:
        return False, "La contraseña debe contener al menos una letra"
    
    if not tiene_numero:
        return False, "La contraseña debe contener al menos un número"
    
    return True, "Datos válidos"

# ===========================================
# VALIDACIÓN DE FORMATO JSON
# ===========================================

@app.before_request
def validate_json():
    """
    Valida que las peticiones POST y PUT contengan JSON válido
    
    Esta función se ejecuta ANTES de cualquier ruta que maneje POST o PUT.
    Si la petición no contiene JSON válido, retorna un error inmediatamente.
    
    ¿Por qué es importante?
    - Evita errores cuando se envían datos en formato incorrecto
    - Da mensajes de error claros al cliente
    - Mejora la seguridad de la API
    """
    # Solo validar peticiones que envían datos (POST, PUT, PATCH)
    if request.method in ['POST', 'PUT', 'PATCH']:
        # Verificar si la petición tiene el header Content-Type correcto
        if not request.is_json:
            return jsonify({
                "error": "Formato de datos incorrecto",
                "mensaje": "La petición debe contener datos en formato JSON",
                "tipo": "error_formato",
                "detalle": "Asegúrate de enviar el header 'Content-Type: application/json'"
            }), 400

# ===========================================
# MANEJO DE ERRORES JWT
# ===========================================

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Maneja tokens JWT expirados
    
    Esta función se ejecuta cuando alguien intenta usar un token que ya expiró.
    En lugar de mostrar un error genérico, da un mensaje claro sobre qué pasó.
    
    Parámetros:
    - jwt_header: información del header del token
    - jwt_payload: información del contenido del token
    
    Retorna:
    - JSON con mensaje de error y código 401 (No autorizado)
    """
    return jsonify({
        "error": "Token expirado",
        "mensaje": "Tu sesión ha expirado. Por favor, inicia sesión nuevamente.",
        "tipo": "error_autenticacion",
        "codigo": "token_expirado"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Maneja tokens JWT inválidos
    
    Esta función se ejecuta cuando el token tiene un formato incorrecto
    o no puede ser verificado (firmado con clave incorrecta, etc.).
    
    Parámetros:
    - error: información sobre el error específico
    
    Retorna:
    - JSON con mensaje de error y código 401 (No autorizado)
    """
    return jsonify({
        "error": "Token inválido",
        "mensaje": "El token de autenticación no es válido.",
        "tipo": "error_autenticacion",
        "codigo": "token_invalido"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Maneja cuando no se proporciona token JWT
    
    Esta función se ejecuta cuando se intenta acceder a una ruta protegida
    sin enviar ningún token de autenticación.
    
    Parámetros:
    - error: información sobre el error específico
    
    Retorna:
    - JSON con mensaje de error y código 401 (No autorizado)
    """
    return jsonify({
        "error": "Token requerido",
        "mensaje": "Se requiere un token de autenticación para acceder a este recurso.",
        "tipo": "error_autenticacion",
        "codigo": "token_faltante"
    }), 401

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
    Obtener tareas del usuario autenticado con búsqueda, filtros y ordenamiento
    """
    # Obtener parámetros de búsqueda y filtros de la URL
    busqueda = request.args.get('busqueda', '').strip()
    estado = request.args.get('estado', '').strip()
    
    # Obtener parámetros de ordenamiento de la URL
    ordenar_por = request.args.get('ordenar_por', 'fecha_creacion').strip()
    orden = request.args.get('orden', 'desc').strip()
    
    # Obtener ID del usuario autenticado
    usuario_id = int(get_jwt_identity())
    
    # Query base: tareas del usuario
    query = Tarea.query.filter_by(usuario_id=usuario_id)
    
    # Aplicar filtro de búsqueda si se proporciona
    if busqueda:
        # Buscar en título Y descripción usando LIKE
        query = query.filter(
            db.or_(
                Tarea.titulo.ilike(f'%{busqueda}%'),
                Tarea.descripcion.ilike(f'%{busqueda}%')
            )
        )
    
    # Aplicar filtro de estado si se proporciona
    if estado:
        if estado.lower() == 'completada':
            query = query.filter(Tarea.completada == True)
        elif estado.lower() == 'pendiente':
            query = query.filter(Tarea.completada == False)
    
    # Aplicar ordenamiento
    if ordenar_por == 'titulo':
        if orden.lower() == 'asc':
            query = query.order_by(Tarea.titulo.asc())
        else:
            query = query.order_by(Tarea.titulo.desc())
    elif ordenar_por == 'fecha_creacion':
        if orden.lower() == 'asc':
            query = query.order_by(Tarea.fecha_creacion.asc())
        else:
            query = query.order_by(Tarea.fecha_creacion.desc())
    elif ordenar_por == 'estado':
        if orden.lower() == 'asc':
            query = query.order_by(Tarea.completada.asc())
        else:
            query = query.order_by(Tarea.completada.desc())
    
    # Ejecutar la consulta
    tareas = query.all()
    
    # Devolver resultados como JSON
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
    
# ===========================================
# MANEJO DE ERRORES DE BASE DE DATOS
# ===========================================

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Maneja errores generales no capturados, especialmente errores de base de datos
    
    Esta función se ejecuta cuando ocurre cualquier error que no fue manejado
    por otros manejadores de errores específicos.
    
    Parámetros:
    - e: el objeto de error que ocurrió
    
    Retorna:
    - JSON con información del error y código de estado 500
    """
    # Imprimir el error en la consola para debugging
    # En producción, esto debería ir a un archivo de log
    print(f"❌ Error no manejado: {str(e)}")
    print(f"🔍 Tipo de error: {type(e).__name__}")
    
    # Verificar si es un error específico de base de datos
    if "database" in str(e).lower() or "sql" in str(e).lower():
        mensaje_error = "Error en la base de datos. Por favor, inténtalo de nuevo."
    else:
        mensaje_error = "Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde."
    
    # Retornar respuesta JSON con información del error
    return jsonify({
        "error": "Error interno del servidor",
        "mensaje": mensaje_error,
        "tipo": "error_interno"
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