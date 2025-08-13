# test_paginacion.py
import requests
import json

# URL base de tu API
BASE_URL = "http://127.0.0.1:5000"

def login_usuario():
    """
    Función para hacer login y obtener token JWT
    """
    datos_login = {
        "username": "testuser",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=datos_login)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def crear_tareas_test(token):
    """
    Crear tareas de prueba para testing
    """
    tareas_test = [
        {"titulo": "Tarea Test 1", "descripcion": "Primera tarea de prueba"},
        {"titulo": "Tarea Test 2", "descripcion": "Segunda tarea de prueba"},
        {"titulo": "Tarea Test 3", "descripcion": "Tercera tarea de prueba"},
        {"titulo": "Tarea Test 4", "descripcion": "Cuarta tarea de prueba"},
        {"titulo": "Tarea Test 5", "descripcion": "Quinta tarea de prueba"},
        {"titulo": "Tarea Test 6", "descripcion": "Sexta tarea de prueba"}
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for tarea in tareas_test:
        response = requests.post(f"{BASE_URL}/tareas", json=tarea, headers=headers)
        if response.status_code == 201:
            print(f"✅ Tarea creada: {tarea['titulo']}")
        else:
            print(f"❌ Error creando tarea: {response.status_code}")

def test_paginacion_basica(token):
    """
    Test básico de paginación
    """
    print("\n🧪 Probando paginación básica...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Probar página 1 con 2 tareas por página
    response = requests.get(f"{BASE_URL}/tareas?pagina=1&limite=2", headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        
        # Verificar estructura de respuesta
        if "tareas" in datos and "paginacion" in datos:
            print("✅ Estructura de respuesta correcta")
            
            # Verificar metadatos de paginación
            paginacion = datos["paginacion"]
            if (paginacion["pagina_actual"] == 1 and 
                paginacion["limite"] == 2 and 
                paginacion["total_paginas"] > 0):
                print("✅ Metadatos de paginación correctos")
                print(f"   Página actual: {paginacion['pagina_actual']}")
                print(f"   Límite: {paginacion['limite']}")
                print(f"   Total tareas: {paginacion['total_tareas']}")
                print(f"   Total páginas: {paginacion['total_paginas']}")
                print(f"   Tiene siguiente: {paginacion['tiene_siguiente']}")
                print(f"   Tiene anterior: {paginacion['tiene_anterior']}")
            else:
                print("❌ Metadatos de paginación incorrectos")
        else:
            print("❌ Estructura de respuesta incorrecta")
    else:
        print(f"❌ Error en request: {response.status_code}")
        print(f"Respuesta: {response.json()}")

def test_paginacion_con_busqueda(token):
    """
    Test de paginación combinada con búsqueda
    """
    print("\n🧪 Probando paginación con búsqueda...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buscar "Test" con paginación
    response = requests.get(f"{BASE_URL}/tareas?busqueda=Test&pagina=1&limite=3", headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        paginacion = datos["paginacion"]
        
        print(f"✅ Búsqueda + paginación funcionando")
        print(f"   Tareas encontradas: {len(datos['tareas'])}")
        print(f"   Total tareas con 'Test': {paginacion['total_tareas']}")
        print(f"   Total páginas: {paginacion['total_paginas']}")
    else:
        print(f"❌ Error en búsqueda + paginación: {response.status_code}")

def test_parametros_invalidos(token):
    """
    Test de parámetros inválidos de paginación
    """
    print("\n🧪 Probando parámetros inválidos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Probar página 0 (debería corregirse a 1)
    response = requests.get(f"{BASE_URL}/tareas?pagina=0&limite=2", headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        if datos["paginacion"]["pagina_actual"] == 1:
            print("✅ Página 0 corregida a página 1")
        else:
            print("❌ Página 0 no fue corregida")
    else:
        print(f"❌ Error con página 0: {response.status_code}")
    
    # Probar límite muy alto (debería limitarse a 100)
    response = requests.get(f"{BASE_URL}/tareas?pagina=1&limite=1000", headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        if datos["paginacion"]["limite"] <= 100:
            print("✅ Límite alto corregido correctamente")
        else:
            print("❌ Límite alto no fue corregido")
    else:
        print(f"❌ Error con límite alto: {response.status_code}")

if __name__ == "__main__":
    print("�� Iniciando tests de paginación...")
    print("=" * 50)
    
    # Login para obtener token
    token = login_usuario()
    if not token:
        print("❌ No se pudo obtener token. Saliendo...")
        exit(1)
    
    print("✅ Login exitoso")
    
    # Crear tareas de prueba
    crear_tareas_test(token)
    
    # Ejecutar tests
    test_paginacion_basica(token)
    test_paginacion_con_busqueda(token)
    test_parametros_invalidos(token)
    
    print("\n" + "=" * 50)
    print("✅ Tests de paginación completados")