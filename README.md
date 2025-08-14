# API de Gestión de Tareas

API REST completa para la gestión de tareas con autenticación JWT, búsqueda avanzada, filtros y paginación.

## Descripción

Esta API permite a los usuarios registrarse, autenticarse y gestionar sus tareas de manera eficiente. Incluye funcionalidades como búsqueda, filtrado, ordenamiento y paginación de resultados.

### Funcionalidades principales:
- Registro e inicio de sesión con autenticación JWT
- CRUD completo de tareas (Crear, Leer, Actualizar, Eliminar)
- Búsqueda de tareas por título y descripción
- Filtrado por estado (completada/pendiente)
- Ordenamiento por título, fecha de creación o estado
- Paginación de resultados
- Validación robusta de datos de entrada

## Demo en Vivo

**URL de la API:** https://api-project-jfbargas.onrender.com

**Para probar la API:**
1. Registra un nuevo usuario usando el endpoint `/registro`
2. Inicia sesión con `/login` para obtener un token JWT
3. Usa el token en el header `Authorization: Bearer <token>` para acceder a los endpoints protegidos


## Tecnologías Utilizadas

### Backend:
- **Python 3.13.4**: Lenguaje de programación principal
- **Flask 3.1.1**: Framework web para crear la API REST
- **Flask-SQLAlchemy**: ORM para manejo de base de datos
- **Flask-JWT-Extended**: Autenticación y autorización con JWT
- **SQLite**: Base de datos relacional (desarrollo)
- **python-dotenv**: Manejo de variables de entorno

### Herramientas de Desarrollo:
- **Git**: Control de versiones
- **GitHub**: Repositorio de código
- **Render**: Plataforma de deploy en la nube
- **Postman**: Testing y documentación de API

### Estructura del Proyecto:
api_tareas/
├── app.py # Aplicación principal Flask
├── models.py # Modelos de base de datos
├── requirements.txt # Dependencias del proyecto
├── Procfile # Configuración para deploy
├── .gitignore # Archivos ignorados por Git
├── crear_usuario.py # Script para crear usuarios de prueba
├── limpiar_db.py # Script para limpiar base de datos
├── test_api.py # Tests de funcionalidades básicas
├── test_busquedas.py # Tests de búsqueda y filtros
├── test_errores.py # Tests de manejo de errores
├── test_ordenamiento.py # Tests de ordenamiento
└── test_paginacion.py # Tests de paginación


## Instalación y Configuración

### Prerrequisitos:
- Python 3.8 o superior
- Git
- Un editor de código (VS Code, PyCharm, etc.)

### Pasos de instalación:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Jairo-Bargas/Api_project.git
   cd Api_project/api_tareas
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Crear archivo de variables de entorno:**
   Crear un archivo `.env` en la carpeta `api_tareas` con el siguiente contenido:
   ```
   FLASK_ENV=development
   SECRET_KEY=tu_clave_secreta_aqui
   DATABASE_URL=sqlite:///tareas.db
   JWT_SECRET_KEY=tu_jwt_clave_secreta_aqui
   ```

6. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

La aplicación estará disponible en: `http://localhost:5000`

## Uso de la API

### Autenticación:
La API utiliza JWT (JSON Web Tokens) para la autenticación. Para acceder a endpoints protegidos, necesitas:

1. **Registrarte** o **iniciar sesión** para obtener un token
2. **Incluir el token** en el header `Authorization: Bearer <token>`

### Endpoints Disponibles:

#### 1. Registro de Usuario
- **URL:** `POST /registro`
- **Descripción:** Crear una nueva cuenta de usuario
- **Body:**
  ```json
  {
    "username": "usuario_ejemplo",
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
  }
  ```

#### 2. Inicio de Sesión
- **URL:** `POST /login`
- **Descripción:** Autenticarse y obtener token JWT
- **Body:**
  ```json
  {
    "username": "usuario_ejemplo",
    "password": "contraseña123"
  }
  ```
- **Respuesta:**
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "mensaje": "Login exitoso"
  }
  ```

#### 3. Crear Tarea
- **URL:** `POST /tareas`
- **Headers:** `Authorization: Bearer <token>`
- **Descripción:** Crear una nueva tarea
- **Body:**
  ```json
  {
    "titulo": "Mi primera tarea",
    "descripcion": "Descripción de la tarea"
  }
  ```

#### 4. Obtener Tareas
- **URL:** `GET /tareas`
- **Headers:** `Authorization: Bearer <token>`
- **Descripción:** Obtener lista de tareas del usuario
- **Parámetros opcionales:**
  - `busqueda`: Buscar por título o descripción
  - `estado`: Filtrar por estado (completada/pendiente)
  - `ordenar_por`: Ordenar por (titulo/fecha_creacion/estado)
  - `orden`: Orden (asc/desc)
  - `pagina`: Número de página
  - `limite`: Tareas por página

#### 5. Actualizar Tarea
- **URL:** `PUT /tareas/<id>`
- **Headers:** `Authorization: Bearer <token>`
- **Descripción:** Actualizar una tarea existente
- **Body:**
  ```json
  {
    "titulo": "Título actualizado",
    "descripcion": "Descripción actualizada",
    "completada": true
  }
  ```

#### 6. Eliminar Tarea
- **URL:** `DELETE /tareas/<id>`
- **Headers:** `Authorization: Bearer <token>`
- **Descripción:** Eliminar una tarea

#### 7. Obtener Usuarios
- **URL:** `GET /usuarios`
- **Descripción:** Obtener lista de usuarios registrados (sin autenticación)

## Ejemplos de Uso

### Ejemplo 1: Registro y Login

**1. Registrar un nuevo usuario:**
```bash
curl -X POST https://api-project-jfbargas.onrender.com/registro \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_prueba",
    "email": "prueba@ejemplo.com",
    "password": "123456"
  }'
```

**2. Iniciar sesión:**
```bash
curl -X POST https://api-project-jfbargas.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_prueba",
    "password": "123456"
  }'
```

### Ejemplo 2: Crear y Obtener Tareas

**1. Crear una tarea (usar el token obtenido del login):**
```bash
curl -X POST https://api-project-jfbargas.onrender.com/tareas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{
    "titulo": "Aprender Flask",
    "descripcion": "Estudiar el framework Flask para crear APIs"
  }'
```

**2. Obtener todas las tareas:**
```bash
curl -X GET https://api-project-jfbargas.onrender.com/tareas \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**3. Buscar tareas con filtros:**

curl -X GET "https://api-project-jfbargas.onrender.com/tareas?busqueda=Flask&estado=pendiente&pagina=1&limite=5" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"


### Ejemplo 3: Usando Postman

1. **Importar la colección** de endpoints
2. **Configurar variables** de entorno para la URL base
3. **Hacer login** para obtener el token
4. **Usar el token** en los headers de las peticiones

### Ejemplo 4: Testing Automatizado

Ejecutar los tests incluidos en el proyecto:

python test_api.py
python test_busquedas.py
python test_ordenamiento.py
python test_paginacion.py

## Información Adicional

### Características Técnicas:
- **Validación robusta** de datos de entrada
- **Manejo de errores** con códigos HTTP apropiados
- **Búsqueda case-insensitive** en títulos y descripciones
- **Filtrado flexible** por estado de tareas
- **Ordenamiento personalizable** por múltiples campos
- **Paginación eficiente** con metadatos completos
- **Autenticación JWT** segura
- **Base de datos SQLite** para desarrollo

### Estructura de Respuestas:
Todas las respuestas siguen un formato consistente:
```json
{
  "mensaje": "Descripción del resultado",
  "datos": { ... },
  "error": "Descripción del error (si aplica)"
}
```

### Códigos de Estado HTTP:
- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **400**: Error en los datos enviados
- **401**: No autorizado (token faltante o inválido)
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

### Testing:
El proyecto incluye una suite completa de tests que cubren:
- Funcionalidades básicas (CRUD)
- Búsqueda y filtros
- Ordenamiento
- Paginación
- Manejo de errores

### Deploy:
La aplicación está desplegada en **Render** y está disponible 24/7.
- **URL de producción:** https://api-project-jfbargas.onrender.com
- **Deploy automático** desde GitHub
- **Variables de entorno** configuradas en Render

## Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request


## Contacto

- **GitHub:** [Jairo-Bargas](https://github.com/Jairo-Bargas)
- **Proyecto:** [API de Gestión de Tareas](https://github.com/Jairo-Bargas/Api_project)