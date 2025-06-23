// Handle Signup
const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const data = {
      firstName: document.getElementById('firstName').value,
      lastName: document.getElementById('lastName').value,
      email: document.getElementById('signupEmail').value,
      password: document.getElementById('signupPassword').value,
      confirmPassword: document.getElementById('confirmPassword').value,
      userType: document.querySelector('input[name="userType"]:checked').value
    };

    if (!data.termsAgreement && !document.getElementById('termsAgreement').checked) {
      alert('Please agree to the terms first.');
      return;
    }

    if (data.password !== data.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    try {
      const res = await fetch('/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        alert("Signup successful!");
        window.location.href = 'login.html';
      } else {
        alert(result.message || "Signup failed.");
      }
    } catch (err) {
      console.error(err);
      alert("Signup error occurred.");
    }
  });
}

// Handle Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const payload = {
      email: document.getElementById('loginEmail').value,
      password: document.getElementById('loginPassword').value
    };

    try {
      const res = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });

      const result = await res.json();

      if (res.ok) {
        alert("Login successful!");
        window.location.href = result.redirect;
      } else {
        alert(result.message || "Login failed.");
      }
    } catch (err) {
      console.error(err);
      alert("Login error occurred.");
    }
  });
}
