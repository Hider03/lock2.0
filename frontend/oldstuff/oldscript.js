const form = document.getElementById("itemForm");
const qrContainer = document.getElementById("qr");
const itemButtonContainer = document.getElementById("item-buttons"); // container for dynamic buttons

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const item = {
    item_description: document.getElementById("item_description").value,
    directions: document.getElementById("directions").value,
    dropoff_location: document.getElementById("dropoff_location").value,
    contact: document.getElementById("contact").value || null,
  };

  const res = await fetch("/items/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });

  const data = await res.json();

  // Clear previous QR
  qrContainer.innerHTML = "";

  // Create QR code
  QRCode.toCanvas(`${window.location.origin}/items/${data.id}`, { width: 200 }, (err, canvas) => {
    if (err) console.error(err);
    qrContainer.appendChild(canvas);

    // Clear previous buttons
    itemButtonContainer.innerHTML = "";

    // Create a dynamic button for this item
    const itemButton = document.createElement("button");
    itemButton.textContent = `VIEW ITEM`;
    itemButton.classList.add("item-link-button");
    itemButton.addEventListener("click", () => {
      window.location.href = `/items/${data.id}`;
    });

    // Create a download button for the QR code
    const downloadButton = document.createElement("button");
    downloadButton.textContent = `DOWNLOAD QR CODE`;
    downloadButton.classList.add("download-button");
    downloadButton.addEventListener("click", () => {
      downloadQRCode(canvas, data.id);
    });

    // Append the buttons to the container
    itemButtonContainer.appendChild(itemButton);
    itemButtonContainer.appendChild(downloadButton);
  });
});

// Function to download QR code as PNG
function downloadQRCode(canvas, itemId) {
  const link = document.createElement('a');
  link.download = `qr-code-item-${itemId}.png`;
  link.href = canvas.toDataURL();
  link.click();
}