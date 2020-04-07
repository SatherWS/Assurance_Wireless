// returns selected applications
function getSelected() {
    var items = document.getElementsByName("selected");
    var is_checked = [];
    for (var i = 0; i < items.length; i++) {
        if (items[i].checked) {
            is_checked.push(items[i]);
        }
    }
    // Return the array if it is non-empty, or null
    return is_checked;
}

var choice = '';

// display accepted choices and apps
function showAccepted() {
    choice = 'accept';
    var selects = getSelected();
    var display = document.getElementById("chosen");
    var add_options = document.getElementById("add-options");
    display.innerHTML = '';
    add_options.innerHTML = '';
    add_options.innerHTML += "<option name=''>Qualifying tax bracket</option>";
    add_options.innerHTML += "<option name=''>Has existing government assistance</option>";
    add_options.innerHTML += "<option name=''>Approved for low cost services only</option>";

    for (var i = 0; i < selects.length; i++) {
        display.innerHTML += "<li>Applicant's Email: " + selects[i].value + '</li>';
    }
    document.getElementById('decision').innerHTML = 'Accept';
}

// display deny choices and apps
function showDenied() {
    choice = 'deny'
    var selects = getSelected();
    var display = document.getElementById("chosen");
    var add_options = document.getElementById("add-options");
    display.innerHTML = '';
    add_options.innerHTML = '';
    add_options.innerHTML += "<option name=''>Provided fradulant information</option>";
    add_options.innerHTML += "<option name=''>Income level was too high</option>";
    add_options.innerHTML += "<option name=''>Geographic location doesn't qualify</option>";

    for (var i = 0; i < selects.length; i++) {
        display.innerHTML += "<li>Applicant's Email: " + selects[i].value + '</li>';
    }
    document.getElementById("decision").innerHTML = 'Deny';
}

// switch to call appropriate function
function processApps() {
    if (choice == 'accept')
        document.getElementById("accept").click();
    else
        document.getElementById("deny").click();
}

// simple function that changes all user application checkboxes to selected
function selectAll(source) {
    var boxes = document.getElementsByName('selected[]');
    for (var i = 0; i < boxes.length(); i++) {
        // change boxes to selected
        boxes[i].checked = source.checked;
    }
}

