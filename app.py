# Importamos la clase Flask desde el paquete flask
from flask import Flask

# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial de Python que indica el nombre del archivo actual
app = Flask(__name__)

# Definimos una ruta (endpoint) para la URL raíz "/"
# Cuando alguien accede a http://localhost:5000/ se ejecuta esta función
@app.route('/')
def inicio():
    return "¡Hola, esta es mi API de tareas!"

# Este bloque hace que la app se ejecute solo si el archivo se ejecuta directamente
if __name__ == '__main__':
    # Iniciamos el servidor en modo debug (útil para desarrollo)
    app.run(debug=True)