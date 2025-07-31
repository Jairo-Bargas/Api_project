# test_api.py
import requests
import json

# URL base de la API
BASE_URL = "http://localhost:5000"

def test_crear_tarea():
    """Prueba crear una nueva tarea"""
    print("🧪 Probando crear tarea...")
    
    datos = {
        "titulo": "Aprender SQLAlchemy",
        "descripcion": "Estudiar cómo funciona SQLAlchemy con Flask"
    }
    
    response = requests.post(f"{BASE_URL}/tareas", json=datos)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)
    
    return response.json()["tarea"]["id"]

def test_obtener_tareas():
    """Prueba obtener todas las tareas"""
    print("🧪 Probando obtener tareas...")
    
    response = requests.get(f"{BASE_URL}/tareas")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_actualizar_tarea(tarea_id):
    """Prueba actualizar una tarea"""
    print(f"🧪 Probando actualizar tarea {tarea_id}...")
    
    datos = {
        "titulo": "Aprender SQLAlchemy - COMPLETADO",
        "descripcion": "Ya estudié cómo funciona SQLAlchemy con Flask",
        "completada": True
    }
    
    response = requests.put(f"{BASE_URL}/tareas/{tarea_id}", json=datos)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_eliminar_tarea(tarea_id):
    """Prueba eliminar una tarea"""
    print(f"🧪 Probando eliminar tarea {tarea_id}...")
    
    response = requests.delete(f"{BASE_URL}/tareas/{tarea_id}")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de la API...")
    print("=" * 50)
    
    # Crear una tarea
    tarea_id = test_crear_tarea()
    
    # Obtener todas las tareas
    test_obtener_tareas()
    
    # Actualizar la tarea
    test_actualizar_tarea(tarea_id)
    
    # Obtener tareas nuevamente para ver el cambio
    test_obtener_tareas()
    
    # Eliminar la tarea
    test_eliminar_tarea(tarea_id)
    
    # Verificar que se eliminó
    test_obtener_tareas()
    
    print("✅ Pruebas completadas!") 