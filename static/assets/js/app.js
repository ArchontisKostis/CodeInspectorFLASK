form = document.getElementById("repo-input-form")
form.addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    showLoading(); // Show loading spinner

    // Manually submit the form after a delay (e.g., 0.5 second)
    setTimeout(function() {
        form.submit();
        }, 500);
});

function showLoading() {
    document.getElementById("loading").style.display = "flex";
}