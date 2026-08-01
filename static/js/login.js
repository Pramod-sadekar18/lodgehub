console.log("login.js loaded");

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");

    if (!form) {
        console.error("loginForm not found");
        return;
    }

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        console.log("Form submitted");

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {

            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
                return null;
            };

            const csrfToken = getCookie('csrftoken');

            const response = await fetch(
                `${window.location.origin}/login/`,
                {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {})
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                }
            );

            let data;
            try {
                data = await response.json();
            } catch (parseError) {
                data = { detail: await response.text() };
            }

            console.log("Response Status:", response.status);
            console.log("Response Data:", data);

            const messageElement = document.getElementById("message");

            if (response.ok) {

                localStorage.setItem("access", data.access);
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh", data.refresh);
                localStorage.setItem("refresh_token", data.refresh);
                localStorage.setItem("isAuthenticated", "true");
                localStorage.setItem("username", data.username);
                localStorage.setItem("email", data.email);

                const redirect = localStorage.getItem("redirectAfterLogin") || "/";
                localStorage.removeItem("redirectAfterLogin");

                window.location.href = redirect;
                return;

            } else {

                if (messageElement) {
                    messageElement.textContent = data.detail || data.message || "Login failed. Please check your credentials.";
                    messageElement.style.color = "#b91c1c";
                } else {
                    alert(data.detail || data.message || "Login failed. Please check your credentials.");
                }

                console.log(data);
            }

        } catch (error) {

            console.error("Login Error:", error);
        }

    });

});