document.addEventListener("DOMContentLoaded", () => {
    const createAccountForm = document.getElementById("create-account-form");
    const createErrorMsg = document.getElementById("error-msg-create-account");

    createAccountForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("new-username").value.trim();
        const password = document.getElementById("new-password").value;

        try {
            const response = await fetch("/api/sign-in/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("User Created");
                createAccountForm.reset();
                window.location.href = "/authentication/";
            } else {

                let messages = [];
                if (data.password) {
                    messages.push(`Password: ${data.password.join(" ")}`);
                }
                if (data.username) {
                    messages.push(`Username: ${data.username.join(" ")}`);
                }
                if (messages.length === 0 && data.detail) {
                    messages.push(data.detail);
                }

                createErrorMsg.textContent = messages.join(" ");
            }
        } catch (err) {
            createErrorMsg.textContent = `Unexpected error: ${err.message || err}`;
            console.error(err);
        }
    });
});
