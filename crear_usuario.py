# crear_usuario.py
import requests
import json

BASE_URL = "http://localhost:5000"

def crear_usuario_test():
    print("�� Creando usuario de prueba...")
    
    datos = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/registro", json=datos)
    
    if response.status_code == 201:
        print("✅ Usuario creado exitosamente")
        print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    else:
        print("❌ Error creando usuario")
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    crear_usuario_test()