document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.querySelector('form[action="/upload"]');
    const manipulationForms = document.querySelectorAll('.container form[action^="/"]');
    const resultContainer = document.querySelector('.container');
    const progressBar = document.getElementById('progress-bar'); // Assume an element with this ID exists for progress visualization

    if (uploadForm) {
        uploadForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            uploadPDF(formData);
            progressBar.style.width = '0%'; // Reset progress bar width before a new upload starts
        });
    }

    manipulationForms.forEach(form => {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const action = this.getAttribute("action");
            const formData = new FormData(this);
            manipulatePDF(action, formData);
        });
    });

    function uploadPDF(formData) {
        let url = '/upload';
        let xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable) {
                let percentage = (e.loaded / e.total) * 100;
                progressBar.style.width = percentage + '%';
            }
        };
        xhr.onload = function() {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.responseText);
                if (data.success) {
                    window.location.href = "/options?filename=" + data.filename;
                } else {
                    alert("Failed to upload PDF. Please try again.");
                }
            } else {
                alert("An error occurred. Please try again.");
            }
        };
        xhr.onerror = function() {
            console.error("Error:", xhr.statusText);
        };
        xhr.send(formData);
    }

    function manipulatePDF(action, formData) {
        fetch(action, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.message) {
                    displayResultMessage(data.message);
                } else if (data.filename) {
                    displayDownloadLink(data.filename);
                } else if (data.text) {
                    displayExtractedText(data.text);
                }
            } else {
                alert("Failed to process PDF. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }

    function displayResultMessage(message) {
        resultContainer.innerHTML = `<p>${message}</p>` + resultContainer.innerHTML;
    }

    function displayDownloadLink(filename) {
        const downloadLink = `<div class="file-result">
                                <h2>Result File</h2>
                                <a href="/static/uploads/${filename}" download>Download ${filename}</a>
                              </div>`;
        resultContainer.innerHTML = downloadLink + resultContainer.innerHTML;
    }

    function displayExtractedText(text) {
        const textResult = `<div class="text-result">
                                <h2>Extracted Text</h2>
                                <textarea readonly>${text}</textarea>
                            </div>`;
        resultContainer.innerHTML = textResult + resultContainer.innerHTML;
    }
});
```