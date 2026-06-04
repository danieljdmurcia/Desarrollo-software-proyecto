// ── Helpers auth ───────────────────────────────────────────────────────────────

function getToken()  { return localStorage.getItem('vulcaria_token'); }
function getUser()   { return JSON.parse(localStorage.getItem('vulcaria_user') || 'null'); }

// ── API carrito ────────────────────────────────────────────────────────────────

async function apiCarrito(method, path = '', body = null) {
    const token = getToken();
    const opts  = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);
    const res  = await fetch(`${API_URL}${path}?token=${token}`, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error en carrito');
    return data;
}

async function cargarCarrito() {
    const token = getToken();
    if (!token) return [];
    try {
        return await apiCarrito('GET', '/carrito');
    } catch { return []; }
}

async function agregarAPI(producto_id, cantidad = 1) {
    return apiCarrito('POST', `/carrito?producto_id=${producto_id}&cantidad=${cantidad}`);
}

async function actualizarAPI(item_id, cantidad) {
    return apiCarrito('PATCH', `/carrito/${item_id}?cantidad=${cantidad}`);
}

async function eliminarAPI(item_id) {
    return apiCarrito('DELETE', `/carrito/${item_id}`);
}

async function vaciarAPI() {
    return apiCarrito('DELETE', '/carrito');
}

// ── Contador del header ────────────────────────────────────────────────────────

async function updateCartCount() {
    const el   = document.getElementById('cart-count');
    if (!el) return;
    const cart = await cargarCarrito();
    const total = cart.reduce((acc, i) => acc + i.cantidad, 0);
    el.textContent = total;
    el.style.display = total > 0 ? 'flex' : 'none';
}

// ── Agregar al carrito ─────────────────────────────────────────────────────────

async function addToCart(producto_id, nombre, precio, imagen_url) {
    const token = getToken();
    if (!token) {
        abrirModal('login');
        return;
    }
    try {
        await agregarAPI(producto_id, 1);
        showCartFeedback();
        await updateCartCount();
        if (document.querySelector('.cart-panel.active')) {
            await renderCart();
        }
    } catch (err) {
        alert(err.message);
    }
}

function showCartFeedback() {
    const btn = document.getElementById('cart-btn');
    if (!btn) return;
    btn.style.background = '#636c83';
    setTimeout(() => btn.style.background = '', 500);
}

// ── Modificar cantidad ─────────────────────────────────────────────────────────

async function changeQty(item_id, delta) {
    const cart = await cargarCarrito();
    const item = cart.find(i => i.id === item_id);
    if (!item) return;
    const nueva = item.cantidad + delta;
    try {
        if (nueva <= 0) {
            await eliminarAPI(item_id);
        } else {
            await actualizarAPI(item_id, nueva);
        }
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message); }
}

async function removeFromCart(item_id) {
    try {
        await eliminarAPI(item_id);
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message); }
}

async function clearCart() {
    try {
        await vaciarAPI();
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message); }
}

// ── Abrir / cerrar panel ───────────────────────────────────────────────────────

async function openCart() {
    const token = getToken();
    if (!token) {
        abrirModal('login');
        return;
    }
    document.querySelector('.cart-panel').classList.add('active');
    document.querySelector('.cart-overlay').classList.add('active');
    await renderCart();
}

function closeCart() {
    document.querySelector('.cart-panel').classList.remove('active');
    document.querySelector('.cart-overlay').classList.remove('active');
}

// ── Render del panel ───────────────────────────────────────────────────────────

async function renderCart() {
    const cart       = await cargarCarrito();
    const container  = document.getElementById('cart-items');
    const totalEl    = document.getElementById('cart-total');
    const confirmBtn = document.getElementById('cart-confirm');
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="cart-empty">
                <p>Tu carrito está vacío</p>
                <p>Agrega productos para comenzar</p>
            </div>`;
        if (totalEl)    totalEl.textContent = '$0';
        if (confirmBtn) confirmBtn.disabled = true;
        return;
    }

    if (confirmBtn) confirmBtn.disabled = false;

    const total = cart.reduce((acc, i) => acc + i.precio * i.cantidad, 0);

    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img
                class="cart-item-img"
                src="${item.imagen_url || '/images/anillo1-removebg-preview.png'}"
                alt="${item.nombre}"
                onerror="this.src='/images/anillo1-removebg-preview.png'"
            >
            <div class="cart-item-info">
                <h4>${item.nombre}</h4>
                <p>$${item.precio.toLocaleString('es-CO')} c/u</p>
                <div class="cart-item-controls">
                    <button onclick="changeQty(${item.id}, -1)">−</button>
                    <span>${item.cantidad}</span>
                    <button onclick="changeQty(${item.id}, 1)">+</button>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">✕</button>
                <span style="font-size:.85rem;color:#f9f9f9;font-weight:600;">
                    $${(item.precio * item.cantidad).toLocaleString('es-CO')}
                </span>
            </div>
        </div>
    `).join('');

    if (totalEl) totalEl.textContent = `$${total.toLocaleString('es-CO')}`;
}

// ── Ir al checkout ─────────────────────────────────────────────────────────────

async function confirmarPedido() {
    const cart  = await cargarCarrito();
    const token = getToken();
    if (!token) { abrirModal('login'); return; }
    if (cart.length === 0) return;
    localStorage.setItem('vulcaria_checkout', JSON.stringify(cart));
    window.location.href = '/Frontend/checkout.html';
}

function comprarDirecto(producto_id, nombre, precio, imagen_url) {
    const token = getToken();
    if (!token) { abrirModal('login'); return; }
    const item = [{ id: producto_id, nombre, precio, imagen_url, cantidad: 1 }];
    localStorage.setItem('vulcaria_checkout', JSON.stringify(item));
    window.location.href = '/Frontend/checkout.html';
}

// ── Init ───────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    document.querySelector('.cart-overlay')?.addEventListener('click', function(e) {
        if (e.target === this) closeCart();
    });
    fetch(`${API_URL}/productos`)
        .then(r => r.json())
        .then(productos => {
            window._productosAPI = {};
            productos.forEach(p => { window._productosAPI[p.nombre] = p; });
        })
        .catch(() => {});
});// ── Helpers auth ───────────────────────────────────────────────────────────────

function getToken()  { return localStorage.getItem('vulcaria_token'); }
function getUser()   { return JSON.parse(localStorage.getItem('vulcaria_user') || 'null'); }

// ── API carrito ────────────────────────────────────────────────────────────────

async function apiCarrito(method, path = '', body = null) {
    const token     = getToken();
    const separator = path.includes('?') ? '&' : '?';
    const opts      = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);
    const res  = await fetch(`${API_URL}${path}${separator}token=${token}`, opts);
    const data = await res.json();
    if (!res.ok) {
        const msg = typeof data.detail === 'string'
            ? data.detail
            : JSON.stringify(data.detail);
        throw new Error(msg || 'Error en carrito');
    }
    return data;
}

async function cargarCarrito() {
    const token = getToken();
    if (!token) return [];
    try {
        return await apiCarrito('GET', '/carrito');
    } catch { return []; }
}

async function agregarAPI(producto_id, cantidad = 1) {
    return apiCarrito('POST', `/carrito?producto_id=${producto_id}&cantidad=${cantidad}`);
}

async function actualizarAPI(item_id, cantidad) {
    return apiCarrito('PATCH', `/carrito/${item_id}?cantidad=${cantidad}`);
}

async function eliminarAPI(item_id) {
    return apiCarrito('DELETE', `/carrito/${item_id}`);
}

async function vaciarAPI() {
    return apiCarrito('DELETE', '/carrito');
}

// ── Contador del header ────────────────────────────────────────────────────────

async function updateCartCount() {
    const el  = document.getElementById('cart-count');
    if (!el) return;
    const cart  = await cargarCarrito();
    const total = cart.reduce((acc, i) => acc + i.cantidad, 0);
    el.textContent   = total;
    el.style.display = total > 0 ? 'flex' : 'none';
}

// ── Agregar al carrito ─────────────────────────────────────────────────────────

async function addToCart(producto_id, nombre, precio, imagen_url) {
    const token = getToken();
    if (!token) {
        abrirModal('login');
        return;
    }
    try {
        await agregarAPI(producto_id, 1);
        showCartFeedback();
        await updateCartCount();
        if (document.querySelector('.cart-panel.active')) {
            await renderCart();
        }
    } catch (err) {
        alert(err.message || 'Error al agregar al carrito');
    }
}

function showCartFeedback() {
    const btn = document.getElementById('cart-btn');
    if (!btn) return;
    btn.style.background = '#636c83';
    setTimeout(() => btn.style.background = '', 500);
}

// ── Modificar cantidad ─────────────────────────────────────────────────────────

async function changeQty(item_id, delta) {
    const cart = await cargarCarrito();
    const item = cart.find(i => i.id === item_id);
    if (!item) return;
    const nueva = item.cantidad + delta;
    try {
        if (nueva <= 0) {
            await eliminarAPI(item_id);
        } else {
            await actualizarAPI(item_id, nueva);
        }
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message || 'Error al actualizar'); }
}

async function removeFromCart(item_id) {
    try {
        await eliminarAPI(item_id);
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message || 'Error al eliminar'); }
}

async function clearCart() {
    try {
        await vaciarAPI();
        await renderCart();
        await updateCartCount();
    } catch (err) { alert(err.message || 'Error al vaciar'); }
}

// ── Abrir / cerrar panel ───────────────────────────────────────────────────────

async function openCart() {
    const token = getToken();
    if (!token) {
        abrirModal('login');
        return;
    }
    document.querySelector('.cart-panel').classList.add('active');
    document.querySelector('.cart-overlay').classList.add('active');
    await renderCart();
}

function closeCart() {
    document.querySelector('.cart-panel').classList.remove('active');
    document.querySelector('.cart-overlay').classList.remove('active');
}

// ── Render del panel ───────────────────────────────────────────────────────────

async function renderCart() {
    const cart       = await cargarCarrito();
    const container  = document.getElementById('cart-items');
    const totalEl    = document.getElementById('cart-total');
    const confirmBtn = document.getElementById('cart-confirm');
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="cart-empty">
                <p>Tu carrito está vacío</p>
                <p>Agrega productos para comenzar</p>
            </div>`;
        if (totalEl)    totalEl.textContent = '$0';
        if (confirmBtn) confirmBtn.disabled = true;
        return;
    }

    if (confirmBtn) confirmBtn.disabled = false;

    const total = cart.reduce((acc, i) => acc + i.precio * i.cantidad, 0);

    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img
                class="cart-item-img"
                src="${item.imagen_url || '/images/anillo1-removebg-preview.png'}"
                alt="${item.nombre}"
                onerror="this.src='/images/anillo1-removebg-preview.png'"
            >
            <div class="cart-item-info">
                <h4>${item.nombre}</h4>
                <p>$${item.precio.toLocaleString('es-CO')} c/u</p>
                <div class="cart-item-controls">
                    <button onclick="changeQty(${item.id}, -1)">−</button>
                    <span>${item.cantidad}</span>
                    <button onclick="changeQty(${item.id}, 1)">+</button>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">✕</button>
                <span style="font-size:.85rem;color:#f9f9f9;font-weight:600;">
                    $${(item.precio * item.cantidad).toLocaleString('es-CO')}
                </span>
            </div>
        </div>
    `).join('');

    if (totalEl) totalEl.textContent = `$${total.toLocaleString('es-CO')}`;
}

// ── Ir al checkout ─────────────────────────────────────────────────────────────

async function confirmarPedido() {
    const cart  = await cargarCarrito();
    const token = getToken();
    if (!token) { abrirModal('login'); return; }
    if (cart.length === 0) return;
    localStorage.setItem('vulcaria_checkout', JSON.stringify(cart));
    window.location.href = '/Frontend/checkout.html';
}

function comprarDirecto(producto_id, nombre, precio, imagen_url) {
    const token = getToken();
    if (!token) { abrirModal('login'); return; }
    const item = [{ id: producto_id, producto_id, nombre, precio, imagen_url, cantidad: 1 }];
    localStorage.setItem('vulcaria_checkout', JSON.stringify(item));
    window.location.href = '/Frontend/checkout.html';
}

// ── Init ───────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    document.querySelector('.cart-overlay')?.addEventListener('click', function(e) {
        if (e.target === this) closeCart();
    });
    fetch(`${API_URL}/productos`)
        .then(r => r.json())
        .then(productos => {
            window._productosAPI = {};
            productos.forEach(p => { window._productosAPI[p.nombre] = p; });
        })
        .catch(() => {});
});
