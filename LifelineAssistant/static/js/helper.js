// simple function that changes all user application checkboxes to selected
function selectAll(source) {
    var boxes = document.getElementsByName('selected[]');
    for (var i = 0; i < boxes.length(); i++) {
        // change boxes to selected
        boxes[i].checked = source.checked;
    }
}

/*
// rows in queue delete script tag later
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const rows = document.querySelectorAll("tr[data-href]");

        rows.forEach(row => {
            row.addEventListener("click", () => {
                window.location.href = row.dataset.href;
            });
        });
    });
</script>
*/