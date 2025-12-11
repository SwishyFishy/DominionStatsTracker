// Add event handler to player 3 name dropdown which requires the otehr player 3 field be filled out if a player 3 is selected
p3Selector = document.getElementById("p3")
p3Selector.addEventListener("change", () => {
    [...document.getElementsByClassName("p3_input")].forEach((input) => {
        if (p3Selector.value != '')
        {
            input.setAttribute("required", true);
        }
        else
        {
            input.removeAttribute("required");
        }
    })
})

// Add event handler to player 4 name dropdown which requires the other player 4 fields and the player 3 fields to be filled out if a player 4 is selected
p4Selector = document.getElementById("p4")
p4Selector.addEventListener("change", () => {
    [...document.getElementsByClassName("p4_input")].forEach((input) => {
        if (p4Selector.value != '')
        {
            input.setAttribute("required", true);
        }
        else
        {
            input.removeAttribute("required");
        }
    })

    if (p4Selector.value != '')
    {
        p3Selector.setAttribute("required", true);
    }
    else
    {
        p3Selector.removeAttribute("required");
    }
})