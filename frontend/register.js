const form = document.getElementById("registerForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const registerUser = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    first_name: document.getElementById("first_name").value,
    last_name: document.getElementById("last_name").value,
    password: document.getElementById("password").value,
    confirm_password: document.getElementById("confirm").value,
  };

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(registerUser),
  });

  if (res.ok) {
    alert("Registration successful!");
    window.location.href = "/login";
  } else {
    const error = await res.json();
    alert(`Error: ${error.detail}`);
  }
});

