document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register-form");
  const errorMsg = document.getElementById("error-msg");

  // Login form submit
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        window.location.href = "/home/";  // Redirect after login
      } else {
        errorMsg.textContent = data.detail || "Login failed. Please try again.";
      }
    } catch (err) {
      errorMsg.textContent = `An error occurred. Try again later. ${err}`;
      console.error(err);
    }
  });
});
