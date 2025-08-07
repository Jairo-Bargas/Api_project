# test_ordenamiento.py
import requests
import json

# LÍNEA 1-2: URL base de la API
BASE_URL = "http://localhost:5000"

# LÍNEAS 4-18: Función para hacer login
def login_usuario():
    """Login para obtener token"""
    print("🔐 Haciendo login...")
    
    # LÍNEAS 7-10: Datos de login
    datos = {
        "username": "testuser",
        "password": "123456"  # ← Usa la contraseña correcta
    }
    
    # LÍNEAS 12-18: Hacer petición de login
    response = requests.post(f"{BASE_URL}/login", json=datos)
    if response.status_code == 200:
        print("✅ Login exitoso")
        return response.json()["access_token"]
    else:
        print("❌ Error en login:", response.json())
        return None

# LÍNEAS 20-40: Función para crear tareas de prueba
def crear_tareas_test(token):
    """Crear tareas de prueba con diferentes fechas y títulos"""
    print("📝 Creando tareas de prueba...")
    
    # LÍNEA 23: Headers con token de autenticación
    headers = {"Authorization": f"Bearer {token}"}
    
    # LÍNEAS 25-32: Lista de tareas para crear
    tareas = [
        {"titulo": "Zebra - Última tarea", "descripcion": "Tarea que empieza con Z"},
        {"titulo": "Aprender Python", "descripcion": "Primera tarea alfabética"},
        {"titulo": "Crear API Flask", "descripcion": "Tarea del medio"},
        {"titulo": "Estudiar SQL", "descripcion": "Otra tarea importante"},
        {"titulo": "Proyecto Python", "descripcion": "Proyecto final"}
    ]
    
    # LÍNEAS 34-39: Crear cada tarea
    for tarea in tareas:
        response = requests.post(f"{BASE_URL}/tareas", json=tarea, headers=headers)
        if response.status_code == 201:
            print(f"✅ Tarea creada: {tarea['titulo']}")
        else:
            print(f"❌ Error creando tarea: {response.json()}")

# LÍNEAS 41-65: Función para probar ordenamiento por título
def test_ordenamiento_titulo(token):
    """Probar ordenamiento por título"""
    print("\n📝 Probando ordenamiento por título...")
    
    # LÍNEA 44: Headers con token
    headers = {"Authorization": f"Bearer {token}"}
    
    # LÍNEAS 46-50: Ordenar por título ascendente (A-Z)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=titulo&orden=asc", headers=headers)
    print(f"Ordenamiento título ASC (A-Z):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")
    
    # LÍNEAS 52-56: Ordenar por título descendente (Z-A)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=titulo&orden=desc", headers=headers)
    print(f"\nOrdenamiento título DESC (Z-A):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")

# LÍNEAS 67-85: Función para probar ordenamiento por fecha
def test_ordenamiento_fecha(token):
    """Probar ordenamiento por fecha"""
    print("\n📅 Probando ordenamiento por fecha...")
    
    # LÍNEA 70: Headers con token
    headers = {"Authorization": f"Bearer {token}"}
    
    # LÍNEAS 72-76: Ordenar por fecha descendente (más recientes primero)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=fecha_creacion&orden=desc", headers=headers)
    print(f"Ordenamiento fecha DESC (más recientes primero):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} ({tarea['fecha_creacion']})")
    
    # LÍNEAS 78-82: Ordenar por fecha ascendente (más antiguas primero)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=fecha_creacion&orden=asc", headers=headers)
    print(f"\nOrdenamiento fecha ASC (más antiguas primero):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} ({tarea['fecha_creacion']})")

# LÍNEAS 87-105: Función para probar ordenamiento por estado
def test_ordenamiento_estado(token):
    """Probar ordenamiento por estado"""
    print("\n🏷️ Probando ordenamiento por estado...")
    
    # LÍNEA 90: Headers con token
    headers = {"Authorization": f"Bearer {token}"}
    
    # LÍNEAS 92-96: Ordenar por estado ascendente (pendientes primero)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=estado&orden=asc", headers=headers)
    print(f"Ordenamiento estado ASC (pendientes primero):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} (Completada: {tarea['completada']})")
    
    # LÍNEAS 98-102: Ordenar por estado descendente (completadas primero)
    response = requests.get(f"{BASE_URL}/tareas?ordenar_por=estado&orden=desc", headers=headers)
    print(f"\nOrdenamiento estado DESC (completadas primero):")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} (Completada: {tarea['completada']})")

# LÍNEAS 107-125: Función para probar ordenamiento combinado
def test_ordenamiento_combinado(token):
    """Probar ordenamiento con búsqueda y filtros"""
    print("\n🎯 Probando ordenamiento combinado...")
    
    # LÍNEA 110: Headers con token
    headers = {"Authorization": f"Bearer {token}"}
    
    # LÍNEAS 112-116: Búsqueda + ordenamiento
    response = requests.get(f"{BASE_URL}/tareas?busqueda=Python&ordenar_por=titulo&orden=asc", headers=headers)
    print(f"Búsqueda 'Python' + ordenamiento título ASC:")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")

# LÍNEAS 127-145: Función principal
if __name__ == "__main__":
    print("🚀 Iniciando pruebas de ordenamiento...")
    print("=" * 50)
    
    # LÍNEA 130: Hacer login
    token = login_usuario()
    if not token:
        print("❌ Error: No se pudo hacer login")
        exit(1)
    
    # LÍNEA 133: Crear tareas de prueba
    crear_tareas_test(token)
    
    # LÍNEAS 135-139: Ejecutar todas las pruebas
    test_ordenamiento_titulo(token)
    test_ordenamiento_fecha(token)
    test_ordenamiento_estado(token)
    test_ordenamiento_combinado(token)
    
    # LÍNEA 141: Mensaje final
    print("\n✅ Pruebas de ordenamiento completadas!")