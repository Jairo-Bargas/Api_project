# app.py

from flask import Flask, jsonify, request  # Importamos Flask y funciones útiles

app = Flask(__name__)  # Creamos la app Flask

tareas = []  # Lista vacía para almacenar tareas (por ahora en memoria, sin base de datos)
proximo_id = 1

# Ruta para obtener todas las tareas
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    return jsonify(tareas)  # Devuelve la lista de tareas en formato JSON

# Ruta para agregar una nueva tarea
@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    global proximo_id
    nueva = request.json
    nueva['id']= proximo_id  # Lee los datos enviados en formato JSON
    tareas.append(nueva) 
    proximo_id += 1 # Agrega la nueva tarea a la lista
    return jsonify({"mensaje": "Tarea agregada", "tarea": nueva}), 201  # Devuelve mensaje + tarea

# Iniciar la app en modo debug
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Ejecuta el servidor Flask
