// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Initialize any variables or states needed
    const uploadForm = document.getElementById("uploadForm");
    const progressBar = document.getElementById("progressBar");
    const resultMessage = document.getElementById("resultMessage");

    // Check if elements exist to avoid errors in pages without these elements
    if (uploadForm && progressBar && resultMessage) {
        uploadForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const formData = new FormData(uploadForm);
            const xhr = new XMLHttpRequest();

            // Update progress bar during the upload
            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    const percentage = (event.loaded / event.total) * 100;
                    progressBar.value = percentage;
                    progressBar.textContent = percentage + '%'; // Fallback for older browsers
                }
            };

            // Handle the response from the server
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    // Process success
                    const response = JSON.parse(xhr.responseText);
                    displayMessage("success", "PDF processed successfully. " + response.message);
                } else {
                    // Process failure
                    displayMessage("error", "Error processing PDF. Please try again.");
                }
            };

            // Handle network errors
            xhr.onerror = function() {
                displayMessage("error", "Network error. Please check your connection and try again.");
            };

            // Set up request and send it
            xhr.open("POST", "/upload-pdf", true);
            xhr.send(formData);
        });
    }

    // Function to display messages
    function displayMessage(type, message) {
        resultMessage.className = type; // 'success' or 'error'
        resultMessage.textContent = message;
        resultMessage.style.display = "block";
    }

    // Optionally, you can add more event listeners or functions to handle other interactions
    // remember to check if elements exist before adding event listeners to avoid errors
});