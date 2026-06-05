// ── Storage ────────────────────────────────────────────────────────────────────

function getCart() {
    return JSON.parse(localStorage.getItem('vulcaria_cart') || '[]');
}

function saveCart(cart) {
    localStorage.setItem('vulcaria_cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

// ── Agregar al carrito ─────────────────────────────────────────────────────────

function addToCart(id, nombre, precio, imagen_url) {
    const cart = getCart();
    const existing = cart.find(i => i.id === id);
    if (existing) {
        existing.cantidad += 1;
    } else {
        cart.push({ id, nombre, precio, imagen_url, cantidad: 1 });
    }
    saveCart(cart);
    showCartFeedback();
}

function showCartFeedback() {
    const btn = document.getElementById('cart-btn');
    if (!btn) return;
    btn.style.background = '#636c83';
    setTimeout(() => btn.style.background = '', 400);
}

// ── Quitar / modificar cantidad ────────────────────────────────────────────────

function removeFromCart(id) {
    saveCart(getCart().filter(i => i.id !== id));
}

function changeQty(id, delta) {
    const cart = getCart();
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.cantidad += delta;
    if (item.cantidad <= 0) {
        saveCart(cart.filter(i => i.id !== id));
    } else {
        saveCart(cart);
    }
}

function clearCart() {
    saveCart([]);
}

// ── Total ──────────────────────────────────────────────────────────────────────

function getTotal() {
    return getCart().reduce((acc, i) => acc + i.precio * i.cantidad, 0);
}

// ── Contador del header ────────────────────────────────────────────────────────

function updateCartCount() {
    const el = document.getElementById('cart-count');
    if (!el) return;
    const total = getCart().reduce((acc, i) => acc + i.cantidad, 0);
    el.textContent = total;
    el.style.display = total > 0 ? 'flex' : 'none';
}

// ── Abrir / cerrar panel ───────────────────────────────────────────────────────

function openCart() {
    document.querySelector('.cart-panel').classList.add('active');
    document.querySelector('.cart-overlay').classList.add('active');
    renderCart();
}

function closeCart() {
    document.querySelector('.cart-panel').classList.remove('active');
    document.querySelector('.cart-overlay').classList.remove('active');
}

// ── Render del panel ───────────────────────────────────────────────────────────

function renderCart() {
    const cart       = getCart();
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
        if (totalEl)    totalEl.textContent = '$0.00';
        if (confirmBtn) confirmBtn.disabled = true;
        return;
    }

    if (confirmBtn) confirmBtn.disabled = false;

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
                    <button onclick="changeQty('${item.id}', -1)">−</button>
                    <span>${item.cantidad}</span>
                    <button onclick="changeQty('${item.id}', 1)">+</button>
                </div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
                <button class="cart-item-remove" onclick="removeFromCart('${item.id}')">✕</button>
                <span style="font-size:.85rem;color:#f9f9f9;font-weight:600;">
                    $${(item.precio * item.cantidad).toLocaleString('es-CO')}
                </span>
            </div>
        </div>
    `).join('');

    if (totalEl) totalEl.textContent = `$${getTotal().toLocaleString('es-CO')}`;
}

// ── Confirmar pedido ───────────────────────────────────────────────────────────

async function confirmarPedido() {
    const cart       = getCart();
    const token      = typeof getToken === 'function' ? getToken() : localStorage.getItem('vulcaria_token');
    const msgEl      = document.getElementById('cart-msg');
    const confirmBtn = document.getElementById('cart-confirm');

    if (cart.length === 0) return;

    if (!token) {
        if (msgEl) {
            msgEl.textContent = 'Debes iniciar sesión para confirmar el pedido';
            msgEl.className   = 'cart-msg error';
        }
        return;
    }

    confirmBtn.disabled     = true;
    confirmBtn.textContent  = 'Procesando...';

    try {
        const resultados = await Promise.all(cart.map(item =>
            fetch(`${API_URL}/pedidos`, {
                method:  'POST',
                headers: {
                    'Content-Type':  'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    producto_id: typeof item.id === 'number' ? item.id : 1,
                    cantidad:    item.cantidad
                })
            })
        ));

        const errores = resultados.filter(r => !r.ok);
        if (errores.length > 0) throw new Error('Algunos productos no pudieron procesarse');

        clearCart();
        if (msgEl) {
            msgEl.textContent = '¡Pedido confirmado! Pronto nos comunicamos contigo.';
            msgEl.className   = 'cart-msg success';
        }
        setTimeout(() => closeCart(), 2500);

    } catch (err) {
        if (msgEl) {
            msgEl.textContent = err.message || 'Error al confirmar el pedido';
            msgEl.className   = 'cart-msg error';
        }
    } finally {
        confirmBtn.disabled    = false;
        confirmBtn.textContent = 'Confirmar pedido';
    }
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
            productos.forEach(p => {
                window._productosAPI[p.nombre] = p;
            });
        })
        .catch(() => {});
});