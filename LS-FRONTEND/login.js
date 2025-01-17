document.querySelector("#login-btn").addEventListener("click", async () => {
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;
  
    try {
      const response = await fetch("http://localhost:8000/api/v1/users/sign-in", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
  
      if (response.ok) {
        const data = await response.json();
        alert(`Welcome, ${data.fullname}`);
        // Optionally redirect the user
        // window.location.href = "index.html";
      } else {
        alert("Invalid credentials. Try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong.");
    }
  });
  