const logo = document.getElementById("logo"); // replace with your logo's ID

logo.addEventListener("click", async (e) => {
  e.preventDefault();

  try {
    const res = await fetch("/userinfo", {
      method: "GET",
      credentials: "include" // sends the JWT cookie
    });

    if (res.ok) {
      // User is logged in → go to profile
      window.location.href = "/profile";
    } else {
      // Not authenticated → go to homepage
      window.location.href = "/";
    }
  } catch (err) {
    // On error (e.g., network issues), just go to homepage
    window.location.href = "/";
  }
});
