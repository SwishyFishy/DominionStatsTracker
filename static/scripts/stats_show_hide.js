// Add event handler to stats menu hide button to hide the menu, show 3- and 4-player games, and show stats menu show button
hideButton = document.getElementById("hide_stats");
hideButton.addEventListener("click", () => {
    document.getElementById("stats").style.width = "0em";
    document.getElementById("show_stats").style.display = "initial";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "table-row";
    });
});

// Add event handler to stats menu show button to show the menu, hide 3- and 4-player games, and hide self
showButton = document.getElementById("show_stats");
showButton.addEventListener("click", () => {
    document.getElementById("stats").style.width = "31.2vw";
    showButton.style.display = "none";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "none";
    });
});