// Configuración de la API
const API_BASE_URL = 'https://api-project-jfbargas.onrender.com';
let currentToken = null;

// Elementos del DOM
const registerForm = document.getElementById('registerForm');
const loginForm = document.getElementById('loginForm');
const createTaskForm = document.getElementById('createTaskForm');
const authStatus = document.getElementById('authStatus');
const tasksList = document.getElementById('tasksList');
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');

// Función para mostrar mensajes
function showMessage(message, type = 'info') {
    authStatus.innerHTML = `<div class="${type}">${message}</div>`;
    setTimeout(() => {
        authStatus.innerHTML = '';
    }, 5000);
}

// Función para hacer peticiones a la API
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.mensaje || data.error || 'Error en la petición');
        }
        
        return data;
    } catch (error) {
        throw new Error(error.message);
    }
}

// Registro de usuario
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('regUsername').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value
    };
    
    try {
        const result = await makeRequest(`${API_BASE_URL}/registro`, {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showMessage('Usuario registrado exitosamente', 'success');
        registerForm.reset();
    } catch (error) {
        showMessage(error.message, 'error');
    }
});

// Login de usuario
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('loginUsername').value,
        password: document.getElementById('loginPassword').value
    };
    
    try {
        const result = await makeRequest(`${API_BASE_URL}/login`, {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        currentToken = result.access_token;
        showMessage('Login exitoso', 'success');
        loginForm.reset();
        loadTasks(); // Cargar tareas después del login
    } catch (error) {
        showMessage(error.message, 'error');
    }
});

createTaskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    console.log('Token actual:', currentToken);
    
    if (!currentToken) {
        showMessage('Debes iniciar sesión primero', 'error');
        return;
    }
    
    const formData = {
        titulo: document.getElementById('taskTitle').value,
        descripcion: document.getElementById('taskDescription').value
    };
    
    const jsonBody = JSON.stringify(formData);
    
    console.log('Datos a enviar:', formData);
    console.log('JSON body:', jsonBody);
    console.log('Headers:', {
        'Authorization': `Bearer ${currentToken}`,
        'Content-Type': 'application/json'
    });
    
    try {
        const result = await makeRequest(`${API_BASE_URL}/tareas`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${currentToken}`
            },
            body: jsonBody
        });
        
        showMessage('Tarea creada exitosamente', 'success');
        createTaskForm.reset();
        loadTasks();
    } catch (error) {
        console.error('Error completo:', error);
        showMessage(error.message, 'error');
    }
});

// Cargar tareas
async function loadTasks() {
    if (!currentToken) {
        tasksList.innerHTML = '<p>Inicia sesión para ver tus tareas</p>';
        return;
    }
    
    try {
        const searchTerm = searchInput.value;
        const statusFilterValue = statusFilter.value;
        
        let url = `${API_BASE_URL}/tareas?pagina=1&limite=20`;
        
        if (searchTerm) {
            url += `&busqueda=${encodeURIComponent(searchTerm)}`;
        }
        
        if (statusFilterValue) {
            url += `&estado=${statusFilterValue}`;
        }
        
        const result = await makeRequest(url, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        displayTasks(result.tareas);
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Mostrar tareas en la interfaz
function displayTasks(tareas) {
    if (tareas.length === 0) {
        tasksList.innerHTML = '<p>No se encontraron tareas</p>';
        return;
    }
    
    tasksList.innerHTML = tareas.map(tarea => `
        <div class="task-item ${tarea.completada ? 'completed' : ''}">
            <h4>${tarea.titulo}</h4>
            <p>${tarea.descripcion}</p>
            <div class="task-meta">
                <span>Estado: ${tarea.completada ? 'Completada' : 'Pendiente'}</span>
                <span>Creada: ${new Date(tarea.fecha_creacion).toLocaleDateString()}</span>
                <div>
                    <button onclick="toggleTaskStatus(${tarea.id}, ${!tarea.completada})">
                        ${tarea.completada ? 'Marcar Pendiente' : 'Marcar Completada'}
                    </button>
                    <button onclick="deleteTask(${tarea.id})" style="background: #e74c3c;">
                        Eliminar
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Cambiar estado de tarea
async function makeRequest(url, options = {}) {
    console.log('URL:', url);
    console.log('Options:', options);
    console.log('Token:', currentToken);
    
    try {
        const requestOptions = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };
        
        if (options.body) {
            requestOptions.body = options.body;
        }
        
        console.log('Request options:', requestOptions);
        
        const response = await fetch(url, requestOptions);
        
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (!response.ok) {
            throw new Error(data.mensaje || data.error || 'Error en la petición');
        }
        
        return data;
    } catch (error) {
        console.error('Error completo:', error);
        throw new Error(error.message);
    }
}

// Eliminar tarea
async function deleteTask(taskId) {
    if (!confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
        return;
    }
    
    try {
        await makeRequest(`${API_BASE_URL}/tareas/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });
        
        showMessage('Tarea eliminada', 'success');
        loadTasks(); // Recargar tareas
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Event listeners para filtros
searchInput.addEventListener('input', () => {
    // Debounce para no hacer muchas peticiones
    clearTimeout(searchInput.timeout);
    searchInput.timeout = setTimeout(loadTasks, 500);
});

statusFilter.addEventListener('change', loadTasks);

// Cargar tareas al iniciar la página
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});