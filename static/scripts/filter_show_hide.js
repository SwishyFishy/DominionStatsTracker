// Add event handler to filter menu hide button to hide the menu, show 3- and 4-player games, and show filter menu show button
hideButton = document.getElementById("hide_filters");
hideButton.addEventListener("click", () => {
    document.getElementById("filters").style.width = "0em";
    document.getElementById("show_filters").style.display = "initial";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "table-row";
    });
});

// Add event handler to filter menu show button to show the menu, hide 3- and 4-player games, and hide self
showButton = document.getElementById("show_filters");
showButton.addEventListener("click", () => {
    document.getElementById("filters").style.width = "31.2vw";
    showButton.style.display = "none";
    [...document.getElementsByClassName("multiplayer")].forEach((element) => {
        element.style.display = "none";
    });
});