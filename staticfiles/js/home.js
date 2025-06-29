document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#entries-table tbody");
  const errorMsg = document.getElementById("error-msg");

  const getPasswordForm = document.getElementById("get-password");
  const addPasswordForm = document.getElementById("Add-password");
  const generatePasswordBtn = document.getElementById("generate-password");


  const token = localStorage.getItem("access_token");

  if (!token) {
    errorMsg.textContent = "No access token. Please log in.";
    return;
  }

if (generatePasswordBtn) {
  generatePasswordBtn.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/generate-password/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Accept": "application/json"
        }
      });

      if (!response.ok) throw new Error("Failed to generate password");

      const data = await response.json();
      // document.getElementById("password").value = data.generated_password;
      alert(`Generated Password: ${data}`)
    } catch (err) {
      console.error(err);
      alert(`Error generating password. ${err}`);
    }
  });
}

  fetch("/api/password-entries/", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch entries.");
      }
      return response.json();
    })
    .then(data => {
      data.forEach(entry => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${entry.site_name}</td>
          <td>${entry.username}</td>
        `;

        tableBody.appendChild(row);
      });
    })
    .catch(err => {
      errorMsg.textContent = err.message;
    });

  function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        return decodeURIComponent(cookie.split("=")[1]);
      }
    }
    return "";
  }

  // Get Password form
  if (getPasswordForm) {
    getPasswordForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const siteName = document.querySelector("#get-password #site_name").value;

      try {
        const response = await fetch(`/api/reveal-password/`, {
          method: "POST",
          headers: {
            "Accept": "application/json",
              "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
            body: JSON.stringify({
            site_name: siteName,
          }),
        });

        if (!response.ok) throw new Error("Failed to retrieve password");

        const data = await response.json();
        alert(`Site: ${siteName}\nPassword: ${data.decrypted_password}`);
      } catch (err) {
        console.error(err);
        alert("Error retrieving password.");
      }
    });
  }

  // Add Password form
  if (addPasswordForm) {
    addPasswordForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const siteName = document.querySelector("#Add-password #site_name").value;
      const username = document.querySelector("#username").value;
      const password = document.querySelector("#password").value;

      try {
        const response = await fetch("/api/password-entries/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({
            site_name: siteName,
            username: username,
            password: password,
          }),
        });

        if (!response.ok) throw new Error("Failed to add password");

        const result = await response.json();
        alert("Password saved successfully!");
        location.reload();  // reload to show new entry in table
      } catch (err) {
        console.error(err);
        alert("Error saving password.");
      }
    });
  }
});
