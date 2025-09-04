const form = document.getElementById("itemForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const item = {
    item_description: document.getElementById("item_description").value,
    directions: document.getElementById("directions").value,
    dropoff_location: document.getElementById("dropoff_location").value,
    contact: document.getElementById("contact").value || null, // optional
  };

  const res = await fetch("/items/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });

  const data = await res.json();

  const qrContainer = document.getElementById("qr");
  qrContainer.innerHTML = "";

  QRCode.toCanvas(
    `${window.location.origin}/items/${data.id}`,
    { width: 200 },
    (err, canvas) => {
      if (err) console.error(err);
      qrContainer.appendChild(canvas);
    }
  );
});
