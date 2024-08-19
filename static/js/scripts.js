document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const facebookIdInput = document.getElementById("facebook_id");

    form.addEventListener("submit", function (event) {
        const facebookId = facebookIdInput.value.trim();

        // Simple validation for Facebook ID
        const idPattern = /^[0-9]+$/; // Only digits
        const usernamePattern = /^[a-zA-Z0-9.]+$/; // Alphanumeric and dots

        if (!idPattern.test(facebookId) && !usernamePattern.test(facebookId)) {
            event.preventDefault();
            alert("Please enter a valid Facebook ID (numeric ID or username).");
            return;
        }

        // Show a loading message or spinner (optional)
        const submitButton = form.querySelector("button[type='submit']");
        submitButton.disabled = true;
        submitButton.textContent = "Analyzing...";
    });
});
