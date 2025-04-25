document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("qr-form");
  const qrPreview = document.getElementById("qr-preview");
  const downloadBtn = document.getElementById("download-btn");
  const downloadLink = document.getElementById("download-link");
  const loading = document.getElementById("loading");

  // Update color display on change
  document
    .getElementById("color_black")
    .addEventListener("input", function (e) {
      document.getElementById("color-black-display").textContent =
        e.target.value;
      document.getElementById("color-black-preview").style.backgroundColor =
        e.target.value;
    });

  document
    .getElementById("color_white")
    .addEventListener("input", function (e) {
      document.getElementById("color-white-display").textContent =
        e.target.value;
      document.getElementById("color-white-preview").style.backgroundColor =
        e.target.value;
    });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Show loading animation
    loading.style.display = "block";
    qrPreview.style.display = "none";
    downloadBtn.style.display = "none";

    // Get form data
    const formData = new FormData(form);

    // Send AJAX request
    fetch("/generate", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Hide loading animation
        loading.style.display = "none";

        // Display QR code
        qrPreview.src = data.image;
        qrPreview.style.display = "block";

        // Update download link
        downloadLink.href = data.image;
        downloadBtn.style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
        loading.style.display = "none";
        alert("An error occurred while generating the QR code.");
      });
  });
});
