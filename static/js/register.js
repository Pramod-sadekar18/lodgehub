console.log("Register JS Loaded");

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const first_name = document.getElementById("first_name").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const mobile_number = document.getElementById("mobile_number").value;
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;

        const message = document.getElementById("message");

        if (password !== confirm_password) {
            message.innerHTML = "Passwords do not match ❌";
            return;
        }

        const userData = {
            first_name: first_name,
            username: username,
            email: email,
            mobile_number: mobile_number,
            password: password,
            confirm_password: confirm_password
        };

        try {

            const response = await fetch(
                "/register/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(userData)
                }
            );

            const data = await response.json();

            console.log("Status:", response.status);
            console.log("Response:", data);

            if (response.ok) {

                message.innerHTML = "Registration Successful ✅";

                form.reset();

                setTimeout(() => {
                    window.location.href = "/login_ui/";
                }, 1000);

            } else {

                message.innerHTML = "Registration Failed ❌";

                console.log(data);
            }

        } catch (error) {

            console.error("Error:", error);

            message.innerHTML = "Server Error ❌";
        }

    });

});