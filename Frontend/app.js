let nextButton = document.getElementById("next");
let prevButton = document.getElementById("prev");
let backButton = document.getElementById("back");
let seeMoreButtons = document.querySelectorAll(".seeMore");
let carousel = document.querySelector(".carousel");
let listHTML = document.querySelector(".carousel .list");

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