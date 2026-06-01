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
        iconSun.style.display  = 'block';
        iconMoon.style.display = 'none';
    } else {
        document.body.classList.remove('light');
        iconSun.style.display  = 'none';
        iconMoon.style.display = 'block';
    }
}

// Aplicar al cargar la página
applyTheme(localStorage.getItem('theme') || 'dark');

themeToggle.addEventListener('click', () => {
    const current = localStorage.getItem('theme') || 'dark';
    const next    = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    applyTheme(next);
});



nextButton.onclick = function () {
    showSlider("next");
};

prevButton.onclick = function () {
    showSlider("prev");
};

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
        carousel.classList.add("showDetail");
    };
});

backButton.onclick = function () {
    carousel.classList.remove("showDetail");
};

seeMoreButtons.forEach(button => {
    button.onclick = function () {
        carousel.classList.add("showDetail");
    };
});

backButton.onclick = function () {
    carousel.classList.remove("showDetail");
}