const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const loginUser = {
    username: document.getElementById("username").value,
    password: document.getElementById("password").value
  };

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(loginUser),
  });

  if (res.ok) {
    alert("Login successful!");

    // 2️⃣ Fetch profile
    // 
    const profileRes = await fetch("/userinfo", {
      method: "GET",
      credentials: "include"  // send the JWT cookie automatically
    });

    if (profileRes.ok) {
      const userData = await profileRes.json();
      console.log("User data:", userData);
      alert(`Welcome ${userData.username}!`);
      window.location.href = "/profile";
    } else {
      alert("Failed to fetch profile.");
    }

  } else {
    const error = await res.json();
    alert(`Error: ${error.detail}`);
  }
});

