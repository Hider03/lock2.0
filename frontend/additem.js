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
    window.location.href = "/youritems";
  } else {
    const error = await res.json();
    alert(`Error: ${error.detail}`);
  }
});

