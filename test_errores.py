# test_errores.py
import requests 
import json

# URL base de la API
BASE_URL = "http://localhost:5000"

def test_errores_validacion():
    """Prueba errores de validación de datos"""
    print("🧪 Probando errores de validación...")
    print("=" * 50)
    
    # Test 1: Datos vacíos
    print("\n1. Probando datos vacíos:")
    response = requests.post(f"{BASE_URL}/registro", json={})
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Campo faltante
    print("\n2. Probando campo faltante:")
    response = requests.post(f"{BASE_URL}/registro", json={
        "username": "juan123",
        "email": "juan@email.com"
        # Falta password
    })
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Username muy corto
    print("\n3. Probando username muy corto:")
    response = requests.post(f"{BASE_URL}/registro", json={
        "username": "ab",  # Solo 2 caracteres
        "email": "juan@email.com",
        "password": "123456"
    })
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Email inválido
    print("\n4. Probando email inválido:")
    response = requests.post(f"{BASE_URL}/registro", json={
        "username": "juan123",
        "email": "email_invalido",  # Sin @
        "password": "123456"
    })
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Password muy corta
    print("\n5. Probando password muy corta:")
    response = requests.post(f"{BASE_URL}/registro", json={
        "username": "juan123",
        "email": "juan@email.com",
        "password": "123"  # Solo 3 caracteres
    })
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")

def test_errores_formato_json():
    """Prueba errores de formato JSON"""
    print("\n🧪 Probando errores de formato JSON...")
    print("=" * 50)
    
    # Test 1: Sin header Content-Type
    print("\n1. Probando sin header Content-Type:")
    response = requests.post(f"{BASE_URL}/registro", 
                           data='{"username": "juan123", "email": "juan@email.com", "password": "123456"}')
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Con header incorrecto
    print("\n2. Probando con header incorrecto:")
    response = requests.post(f"{BASE_URL}/registro", 
                           headers={'Content-Type': 'text/plain'},
                           data='{"username": "juan123", "email": "juan@email.com", "password": "123456"}')
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")

def test_errores_autenticacion():
    """Prueba errores de autenticación JWT"""
    print("\n🧪 Probando errores de autenticación...")
    print("=" * 50)
    
    # Test 1: Sin token
    print("\n1. Probando sin token:")
    response = requests.get(f"{BASE_URL}/tareas")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Token inválido
    print("\n2. Probando token inválido:")
    headers = {"Authorization": "Bearer token_invalido_123"}
    response = requests.get(f"{BASE_URL}/tareas", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")

def test_errores_recurso_no_encontrado():
    """Prueba errores de recurso no encontrado"""
    print("\n🧪 Probando errores de recurso no encontrado...")
    print("=" * 50)
    
    # Test 1: URL inexistente
    print("\n1. Probando URL inexistente:")
    response = requests.get(f"{BASE_URL}/ruta_inexistente")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Método no permitido
    print("\n2. Probando método no permitido:")
    response = requests.put(f"{BASE_URL}/registro", json={})
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de manejo de errores...")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    test_errores_validacion()
    test_errores_formato_json()
    test_errores_autenticacion()
    test_errores_recurso_no_encontrado()
    
    print("\n✅ Pruebas de errores completadas!")
    print("\n📝 Resumen de lo que probamos:")
    print("- Validación de datos de usuario")
    print("- Formato JSON de peticiones")
    print("- Autenticación JWT")
    print("- Recursos no encontrados")