// Find relevant elements
const type_selector = document.getElementById("kingdom_type");
const sets = document.getElementById("sets");
const notes = document.getElementById("notes");

// Add event listener to control which notes field is used based on the game type
type_selector.addEventListener("change", () => {
    if (type_selector.value == "RSo10")
    {
        sets.disabled = false;
        notes.disabled = true;
        notes.value = "";
    }
    else
    {
        sets.disabled = true;
        sets.value = "";
        notes.disabled = false;
    }
})