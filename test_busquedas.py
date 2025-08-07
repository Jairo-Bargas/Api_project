# test_busqueda.py
import requests
import json

# URL base de la API
BASE_URL = "http://localhost:5000"

def login_usuario():
    """Login para obtener token"""
    print("🔐 Haciendo login...")
    
    datos = {
        "username": "testuser",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=datos)
    if response.status_code == 200:
        print("✅ Login exitoso")
        return response.json()["access_token"]
    else:
        print("❌ Error en login:", response.json())
        return None

def crear_tareas_test(token):
    """Crear tareas de prueba"""
    print("📝 Creando tareas de prueba...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    tareas = [
        {"titulo": "Aprender Python", "descripcion": "Estudiar sintaxis básica de Python"},
        {"titulo": "Crear API Flask", "descripcion": "Desarrollar API REST con Flask"},
        {"titulo": "Estudiar SQL", "descripcion": "Aprender consultas SQL básicas"},
        {"titulo": "Proyecto Python", "descripcion": "Crear aplicación web con Python"},
        {"titulo": "Hacer ejercicio", "descripcion": "Ir al gimnasio y hacer cardio"}
    ]
    
    for tarea in tareas:
        response = requests.post(f"{BASE_URL}/tareas", json=tarea, headers=headers)
        if response.status_code == 201:
            print(f"✅ Tarea creada: {tarea['titulo']}")
        else:
            print(f"❌ Error creando tarea: {response.json()}")

def test_busqueda_basica(token):
    """Probar búsqueda básica"""
    print("\n🔍 Probando búsqueda básica...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buscar "Python"
    response = requests.get(f"{BASE_URL}/tareas?busqueda=Python", headers=headers)
    print(f"Búsqueda 'Python': {len(response.json())} resultados")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")
    
    # Buscar "API"
    response = requests.get(f"{BASE_URL}/tareas?busqueda=API", headers=headers)
    print(f"\nBúsqueda 'API': {len(response.json())} resultados")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")
    
    # Buscar "estudiar"
    response = requests.get(f"{BASE_URL}/tareas?busqueda=estudiar", headers=headers)
    print(f"\nBúsqueda 'estudiar': {len(response.json())} resultados")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")

def test_filtro_estado(token):
    """Probar filtro por estado"""
    print("\n🏷️ Probando filtro por estado...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener tareas pendientes
    response = requests.get(f"{BASE_URL}/tareas?estado=pendiente", headers=headers)
    print(f"Tareas pendientes: {len(response.json())}")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} (Completada: {tarea['completada']})")
    
    # Obtener tareas completadas
    response = requests.get(f"{BASE_URL}/tareas?estado=completada", headers=headers)
    print(f"\nTareas completadas: {len(response.json())}")
    for tarea in response.json():
        print(f"  - {tarea['titulo']} (Completada: {tarea['completada']})")

def test_busqueda_combinada(token):
    """Probar búsqueda + filtro combinados"""
    print("\n🎯 Probando búsqueda + filtro combinados...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buscar "Python" en tareas pendientes
    response = requests.get(f"{BASE_URL}/tareas?busqueda=Python&estado=pendiente", headers=headers)
    print(f"Búsqueda 'Python' + pendientes: {len(response.json())} resultados")
    for tarea in response.json():
        print(f"  - {tarea['titulo']}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de búsqueda...")
    print("=" * 50)
    
    # Login
    token = login_usuario()
    if not token:
        print("❌ Error: No se pudo hacer login")
        exit(1)
    
    # Crear tareas de prueba
    crear_tareas_test(token)
    
    # Probar búsqueda
    test_busqueda_basica(token)
    test_filtro_estado(token)
    test_busqueda_combinada(token)
    
    print("\n✅ Pruebas de búsqueda completadas!")