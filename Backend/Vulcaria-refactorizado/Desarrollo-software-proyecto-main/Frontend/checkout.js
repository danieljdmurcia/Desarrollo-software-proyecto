const API_URL_CO = window.API_URL || 'https://expert-spork-wrvpqg4prv7xfgxj6-8000.app.github.dev';

// ── Datos del checkout ─────────────────────────────────────────────────────────

function getCheckoutItems() {
    return JSON.parse(localStorage.getItem('vulcaria_checkout') || '[]');
}

function getToken() { return localStorage.getItem('vulcaria_token'); }
function getUser()  { return JSON.parse(localStorage.getItem('vulcaria_user') || 'null'); }

// ── Render de productos ────────────────────────────────────────────────────────

function renderProductos() {
    const items     = getCheckoutItems();
    const container = document.getElementById('checkout-items');
    const subtotalEl = document.getElementById('resumen-subtotal');
    const totalEl    = document.getElementById('resumen-total');
    const itemCountEl = document.getElementById('resumen-items');

    if (!items.length) {
        window.location.href = '/Frontend/index.html';
        return;
    }

    const subtotal = items.reduce((acc, i) => acc + i.precio * i.cantidad, 0);
    const envio    = 0;
    const total    = subtotal + envio;

    container.innerHTML = items.map(item => `
        <div class="checkout-item">
            <img
                src="${item.imagen_url || '/images/anillo1-removebg-preview.png'}"
                alt="${item.nombre}"
                onerror="this.src='/images/anillo1-removebg-preview.png'"
            >
            <div class="checkout-item-info">
                <h4>${item.nombre}</h4>
                <p>Cantidad: ${item.cantidad} &nbsp;·&nbsp; $${item.precio.toLocaleString('es-CO')} c/u</p>
            </div>
            <div class="checkout-item-price">
                $${(item.precio * item.cantidad).toLocaleString('es-CO')}
            </div>
        </div>
    `).join('');

    if (subtotalEl)  subtotalEl.textContent  = `$${subtotal.toLocaleString('es-CO')}`;
    if (totalEl)     totalEl.textContent     = `$${total.toLocaleString('es-CO')}`;
    if (itemCountEl) itemCountEl.textContent = `${items.reduce((a, i) => a + i.cantidad, 0)} producto(s)`;
}

// ── Métodos de pago ────────────────────────────────────────────────────────────

function seleccionarMetodo(metodo) {
    document.querySelectorAll('.metodo-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.form-pago').forEach(f => f.classList.remove('active'));
    document.querySelector(`.metodo-btn[data-metodo="${metodo}"]`).classList.add('active');
    document.getElementById(`form-${metodo}`)?.classList.add('active');
    document.getElementById('btn-pagar').disabled = false;
}

// ── Confirmar pago ─────────────────────────────────────────────────────────────

async function confirmarPago() {
    const metodoActivo = document.querySelector('.metodo-btn.active');
    if (!metodoActivo) {
        alert('Selecciona un método de pago');
        return;
    }

    const btn = document.getElementById('btn-pagar');
    btn.disabled    = true;
    btn.textContent = 'Procesando...';

    try {
        const items = getCheckoutItems();
        const token = getToken();

        // Crear pedidos en la BD
        await Promise.all(items.map(item =>
            fetch(`${API_URL_CO}/pedidos`, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    producto_id: item.producto_id || item.id,
                    cantidad:    item.cantidad
                })
            })
        ));

        // Vaciar carrito en BD si hay sesión
        if (token) {
            await fetch(`${API_URL_CO}/carrito?token=${token}`, { method: 'DELETE' });
        }

        // Limpiar localStorage
        localStorage.removeItem('vulcaria_checkout');

        // Mostrar confirmación
        mostrarConfirmacion();

    } catch (err) {
        btn.disabled    = false;
        btn.textContent = 'Confirmar pago';
        alert('Error al procesar el pago. Intenta de nuevo.');
    }
}

// ── Modal de confirmación ──────────────────────────────────────────────────────

function mostrarConfirmacion() {
    document.getElementById('confirm-overlay').classList.add('active');
}

// ── Init ───────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const token = getToken();
    if (!token) {
        window.location.href = '/Frontend/index.html';
        return;
    }

    const usuario = getUser();
    if (usuario) {
        const nombreEl = document.getElementById('nombre-usuario');
        if (nombreEl) nombreEl.textContent = usuario.nombre;
    }

    renderProductos();
});