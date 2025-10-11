// profile.js
async function loadProfile() {
  const res = await fetch("/userinfo", {
    method: "GET",
    credentials: "include"
  });

  if (res.ok) {
    const user = await res.json();
    document.getElementById("userInfo").textContent =
      `${user.username}`;
  } else {
    window.location.href = "/login"; // redirect if not authenticated
  }
}

loadProfile();
