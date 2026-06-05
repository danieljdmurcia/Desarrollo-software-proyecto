let nextButton = document.getElementById("next");
let prevButton = document.getElementById("prev");
let backButton = document.getElementById("back");
let seeMoreButtons = document.querySelectorAll(".seeMore");
let carousel = document.querySelector(".carousel");
let listHTML = document.querySelector(".carousel .list");

// ── MODO CLARO/OSCURO ──
const themeToggle = document.getElementById('themeToggle');
const iconSun     = document.getElementById('iconSun');
const iconMoon    = document.getElementById('iconMoon');

function applyTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light');
        if (iconSun)  iconSun.style.display  = 'block';
        if (iconMoon) iconMoon.style.display = 'none';
    } else {
        document.body.classList.remove('light');
        if (iconSun)  iconSun.style.display  = 'none';
        if (iconMoon) iconMoon.style.display = 'block';
    }
}

applyTheme(localStorage.getItem('theme') || 'dark');

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const current = localStorage.getItem('theme') || 'dark';
        const next    = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', next);
        applyTheme(next);
    });
}

if (nextButton) {
    nextButton.onclick = function () {
        showSlider("next");
    };
}

if (prevButton) {
    prevButton.onclick = function () {
        showSlider("prev");
    };
}

function showSlider(type) {
    let items = document.querySelectorAll(".carousel .list .item");
    if (type === "next") {
        listHTML.appendChild(items[0]);
    } else {
        listHTML.prepend(items[items.length - 1]);
    }
}

seeMoreButtons.forEach((button) => {
    button.onclick = function () {
        if (carousel) carousel.classList.add("showDetail");
    };
});

if (backButton) {
    backButton.onclick = function () {
        if (carousel) carousel.classList.remove("showDetail");
    };
}

// ── SESIÓN ──
function verificarSesion() {
    const usuarioStr     = localStorage.getItem("usuario");
    const labelLogin     = document.getElementById("label-login");
    const btnLogin       = document.getElementById("btn-login");
    const dropdownSesion = document.getElementById("dropdown-sesion");
    const btnCerrar      = document.getElementById("btn-cerrar-sesion");
    const btnAdmin       = document.getElementById("btn-admin-panel");   // ← nuevo

    if (usuarioStr && labelLogin) {
        const u = JSON.parse(usuarioStr);
        labelLogin.textContent = u.usuario || u.nombre;
        btnLogin.href  = "#";
        btnLogin.title = u.usuario || u.nombre;

        if (dropdownSesion) dropdownSesion.removeAttribute("style");

        // ── Mostrar enlace al panel admin solo si es @vulcaria ──
        if (btnAdmin) {
            if (u.es_admin) {
                btnAdmin.style.display = "inline-flex";
            } else {
                btnAdmin.style.display = "none";
            }
        }

        if (btnCerrar) {
            btnCerrar.addEventListener("mouseover", () => {
                btnCerrar.style.color = "#ff4444";
            });
            btnCerrar.addEventListener("mouseout", () => {
                btnCerrar.style.color = "#e07070";
            });
            btnCerrar.addEventListener("click", (e) => {
                e.preventDefault();
                localStorage.removeItem("token");
                localStorage.removeItem("usuario");
                window.location.reload();
            });
        }
    } else {
        if (dropdownSesion) dropdownSesion.style.display = "none";
        if (btnAdmin) btnAdmin.style.display = "none";
    }
}
verificarSesion();