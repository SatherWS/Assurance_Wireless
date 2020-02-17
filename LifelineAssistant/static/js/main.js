// Toggle chat window
var togMenu = false;
function showBot() {
    togMenu = !togMenu;
    var menu =  document.getElementById("bot");
    var button = document.getElementById("bot-block");
    if (togMenu == true) {
        menu.style.height = "80vh";
        menu.style.border = "solid 1px";
        button.style.display = "none";

    }
    else {
        menu.style.height = "0";
        menu.style.border = "none";
        button.style.display = "block";
    }
} 