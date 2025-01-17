document.querySelector("#submit-btn").addEventListener("click", async () => {
    const fullname = document.querySelector("#fullname").value;
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;
    const confirmPassword = document.querySelector("#confirm-password").value;
    const mobileNumber=document.querySelector("#mobile-no").value;
  
    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:8000/api/v1/users/sign-up", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fullname, email, password }),
      });
  
      if (response.ok) {
        alert("Account created successfully!");
        window.location.href = "login.html"; // Redirect to login page
      } else {
        alert("Failed to create account. Try again.");
      }
    } catch (error) {
      console.error("Sign-up error:", error);
      alert("Something went wrong.");
    }
  });
  