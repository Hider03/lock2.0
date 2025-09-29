const form = document.getElementById("addItemForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const ItemCreate = {
    item_description: document.getElementById("item_description").value,
    directions: document.getElementById("directions").value,
    dropoff_location: document.getElementById("dropoff_location").value,
    contact: document.getElementById("contact").value
  };

  const res = await fetch("/additem", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ItemCreate),
  });



  if (res.ok) {
    alert("Item has been added!");

    // show the user their public link in a qr code through the api call 
    const item = await res.json();
      // Fetch the QR code image
    const qrRes = await fetch(`/qrcode/public/${item.public_id}`, { credentials: "include" });
    if (qrRes.ok) {
        const blob = await qrRes.blob();
        const url = URL.createObjectURL(blob);

        // Display the QR code on the page
        const qrImg = document.createElement("img");
        qrImg.src = url;
        document.body.appendChild(qrImg);

        // Optionally show public link
        const link = document.createElement("a");
        const baseUrl = window.location.origin;
        link.href = `${baseUrl}/pub/getitem/${item.public_id}`;
        link.textContent = "Public Item Link";
        document.body.appendChild(link);
    }
  } else {
    const error = await res.json();
    alert(`Error: ${error.detail}`);
  }
});

