async function loadItems() {
  // check if user is logged in
  const res = await fetch("/userinfo", { method: "GET", credentials: "include" });
  if (!res.ok) {
    window.location.href = "/login";
    return;
  }

  // fetch items
  const itemsRes = await fetch("/priv/getitems", { method: "GET", credentials: "include" });
  const items = await itemsRes.json();
  const itemsList = document.getElementById("itemsList");
  itemsList.innerHTML = ""; // clear loading text

  if (!items || items.length === 0) {
    itemsList.textContent = "You have no items yet.";
    return;
  }

  for (const item of items) {
    // ✅ fetch QR image properly
    const qrRes = await fetch(`/qrcode/public/${item.id}`, { credentials: "include" });
    let qrUrl = "";
    if (qrRes.ok) {
      const blob = await qrRes.blob();
      qrUrl = URL.createObjectURL(blob);
    }

    const card = document.createElement("div");
    card.className = "item-card";

    card.innerHTML = `
      <h3>
        <a href="/priv/getitem/${item.id}" class="item-link">
          ${item.item_description}
        </a>
      </h3>
      <p class="item-info"><strong>Directions:</strong> ${item.directions}</p>
      <p class="item-info"><strong>Drop-off Location:</strong> ${item.dropoff_location}</p>
      <p class="item-info"><strong>Contact:</strong> ${item.contact ?? "N/A"}</p>
      <p class="item-actions">
        <a href="/priv/getitem/${item.id}" class="item-link">Edit item</a>
        |
        <a href="/pub/getitem/${item.id}" class="item-link">PUBLIC</a>
        ${
          qrUrl
            ? `| <a href="${qrUrl}" class="item-link" target="_blank"> Download [QR]</a>`
            : ""
        }
        |
        <a href="/remove/${item.id}" class="item-link">Remove</a>
      </p>
    `;

    // ✅ add QR image inline (optional)
    if (qrUrl) {
      const qrImg = document.createElement("img");
      qrImg.src = qrUrl;
      qrImg.alt = "QR Code";
      qrImg.style.width = "120px";
      qrImg.style.display = "block";
      card.appendChild(qrImg);
    }

    itemsList.appendChild(card);
  }
}

loadItems();
