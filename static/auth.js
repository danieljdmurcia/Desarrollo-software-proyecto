const API_URL = 'https://expert-spork-wrvpqg4prv7xfgxj6-8000.app.github.dev';

function getToken() { return localStorage.getItem('vulcaria_token'); }
function getUser()  { return JSON.parse(localStorage.getItem('vulcaria_user') || 'null'); }

function saveSession(data) {
    localStorage.setItem('vulcaria_token', data.access_token);
    localStorage.setItem('vulcaria_user', JSON.stringify(data.usuario));
}

function clearSession() {
    localStorage.removeItem('vulcaria_token');
    localStorage.removeItem('vulcaria_user');
}

function abrirModal(tab = 'login') {
    document.querySelector('.auth-overlay').classList.add('active');
    switchTab(tab);
}

function cerrarModal() {
    document.querySelector('.auth-overlay').classList.remove('active');
    limpiarMensajes();
}

function switchTab(tab) {
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    document.querySelector(`.auth-tab[data-tab="${tab}"]`)?.classList.add('active');
    document.getElementById(`form-${tab}`)?.classList.add('active');
    limpiarMensajes();
}

function limpiarMensajes() {
    document.querySelectorAll('.auth-msg').forEach(m => {
        m.className = 'auth-msg';
        m.textContent = '';
    });
}

function mostrarMsg(id, texto, tipo) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = texto;
    el.className = `auth-msg ${tipo}`;
}

function actualizarHeader() {
    const contenedor = document.getElementById('auth-header');
    if (!contenedor) return;
    const usuario = getUser();
    if (usuario) {
        contenedor.innerHTML = `
            <div class="auth-user-info">
                <span>Hola, ${usuario.nombre.split(' ')[0]}</span>
                <button onclick="logout()">Cerrar sesión</button>
            </div>`;
    } else {
        contenedor.innerHTML = `
            <button class="btn-auth" onclick="abrirModal('login')">Iniciar sesión</button>`;
    }
}

function logout() {
    clearSession();
    actualizarHeader();
}

async function registro(e) {
    e.preventDefault();
    const nombre   = document.getElementById('reg-nombre').value;
    const email    = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    try {
        const res  = await fetch(`${API_URL}/auth/registro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, email, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error al registrarse');
        saveSession(data);
        actualizarHeader();
        cerrarModal();
    } catch (err) {
        mostrarMsg('msg-registro', err.message, 'error');
    }
}

async function login(e) {
    e.preventDefault();
    const email    = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    try {
        const res  = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Credenciales incorrectas');
        saveSession(data);
        actualizarHeader();
        cerrarModal();
    } catch (err) {
        mostrarMsg('msg-login', err.message, 'error');
    }
}

async function recuperarPassword(e) {
    e.preventDefault();
    const email = document.getElementById('rec-email').value;
    try {
        const res  = await fetch(`${API_URL}/auth/recuperar-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        mostrarMsg('msg-recuperar', data.mensaje, 'success');
    } catch {
        mostrarMsg('msg-recuperar', 'Error al enviar el correo', 'error');
    }
}

async function resetPassword(e) {
    e.preventDefault();
    const token    = new URLSearchParams(window.location.search).get('token');
    const password = document.getElementById('reset-password').value;
    try {
        const res  = await fetch(`${API_URL}/auth/reset-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, nueva_password: password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error al restablecer');
        mostrarMsg('msg-reset', data.mensaje, 'success');
        setTimeout(() => window.location.href = '/', 2000);
    } catch (err) {
        mostrarMsg('msg-reset', err.message, 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    actualizarHeader();
    const token = new URLSearchParams(window.location.search).get('token');
    if (token) abrirModal('reset');
    document.querySelector('.auth-overlay')?.addEventListener('click', function(e) {
        if (e.target === this) cerrarModal();
    });
});