Array.from(document.getElementsByClassName("sourcecontainer")).forEach(function(el) {
    var button = el.getElementsByClassName("sourcebutton")[0];
    var icon = el.getElementsByClassName("expandicon")[0];
    var source = el.getElementsByClassName("source")[0];

    button.addEventListener("click", function(e) {
        e.preventDefault();
        source.classList.toggle("hidden");
        icon.classList.toggle("active");
    });
});
