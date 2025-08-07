# limpiar_db.py
import requests
import json

BASE_URL = "http://localhost:5000"

def login_usuario():
    datos = {
        "username": "testuser",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=datos)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def limpiar_tareas():
    print("🧹 Limpiando tareas de prueba...")
    
    token = login_usuario()
    if not token:
        print("❌ Error: No se pudo hacer login")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener todas las tareas
    response = requests.get(f"{BASE_URL}/tareas", headers=headers)
    if response.status_code == 200:
        tareas = response.json()
        print(f"�� Encontradas {len(tareas)} tareas")
        
        # Eliminar cada tarea
        for tarea in tareas:
            tarea_id = tarea['id']
            delete_response = requests.delete(f"{BASE_URL}/tareas/{tarea_id}", headers=headers)
            if delete_response.status_code == 200:
                print(f"🗑️ Eliminada tarea: {tarea['titulo']}")
            else:
                print(f"❌ Error eliminando tarea {tarea_id}")
        
        print("✅ Limpieza completada")
    else:
        print("❌ Error obteniendo tareas")

if __name__ == "__main__":
    limpiar_tareas()