let usernameInput = document.getElementById("username");
let passwordInput = document.getElementById("password");

if (!usernameInput || !passwordInput) {
    console.error("Lỗi: Không tìm thấy input!");
} else {
    let username = usernameInput.value;
    let password = passwordInput.value;
}



document.getElementById("registerBtn").addEventListener("click", function () {
    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;
    const message = document.getElementById("message");

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        message.textContent = data.message;
        message.style.color = response.ok ? "green" : "red";
    })
    .catch(error => console.error("Lỗi:", error));
});

document.getElementById("loginBtn").addEventListener("click", async function () {
    let username = document.getElementById("username")?.value;
    let password = document.getElementById("password")?.value;

    if (!username || !password) {
        alert("Vui lòng nhập đủ thông tin!");
        return;
    }

    let response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    let result = await response.json();
    console.log(result);
    alert(result.message || result.error);
});


fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    })
})
.then(response => response.json())
.then(data => alert(data.message))
.catch(error => console.error("Lỗi:", error));

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginBtn").addEventListener("click", function () {
        let username = document.getElementById("username")?.value;
        let password = document.getElementById("password")?.value;

        if (!username || !password) {
            alert("Vui lòng nhập đầy đủ thông tin!");
            return;
        }

        console.log(username, password); // Kiểm tra xem có lấy được giá trị không
    });
});
