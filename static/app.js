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