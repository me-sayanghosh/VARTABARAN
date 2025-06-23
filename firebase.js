async function sendOTP(email) {
  const res = await fetch("http://localhost:5000/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  });
  const data = await res.json();
  alert(data.message);
}

async function verifyOTP(email, otp) {
  const res = await fetch("http://localhost:5000/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp })
  });
  const data = await res.json();
  alert(data.verified ? "Verified!" : data.message);
}
