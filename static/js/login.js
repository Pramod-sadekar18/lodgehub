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

            const response = await fetch(
                "http://127.0.0.1:114/login/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                }
            );

            const data = await response.json();

            console.log("Response Status:", response.status);
            console.log("Response Data:", data);

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

                alert("Login Failed");
                console.log(data);
            }

        } catch (error) {

            console.error("Login Error:", error);
        }

    });

});