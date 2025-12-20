statsPanel = document.getElementById("stats");

// Add event handler to stats menu hide button to hide the menu, show 3- and 4-player games, and show stats menu show button
hideButton = document.getElementById("hide_stats");
hideButton.addEventListener("click", () => {
    statsPanel.style.width = "0em";
    statsPanel.classList.add("animate_slide_right");
    statsPanel.classList.remove("animate_slide_left");
    document.getElementById("show_stats").style.display = "initial";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "table-row";
    });
});

// Add event handler to stats menu show button to show the menu, hide 3- and 4-player games, and hide self
showButton = document.getElementById("show_stats");
showButton.addEventListener("click", () => {
    statsPanel.style.width = "31.2vw";
    statsPanel.classList.add("animate_slide_left");
    statsPanel.classList.remove("animate_slide_right");
    showButton.style.display = "none";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "none";
    });
});