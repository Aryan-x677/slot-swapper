const API_BASE = "https://slot-swapper.onrender.com"; 
let token = "";

async function signup() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
  alert(res.ok ? "Signup successful!" : "Signup failed!");
}

async function login() {
  const email = document.getElementById("email").value;  // match backend
  const password = document.getElementById("password").value;

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();
  if (res.ok && data.access_token) {
    token = data.access_token;
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("dashboard").classList.remove("hidden");
    fetchEvents();
  } else {
    alert("Login failed: " + (data.detail || "Unknown error"));
  }
}

async function fetchEvents() {
  const res = await fetch(`${API_BASE}/events/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const events = await res.json();
  const list = document.getElementById("events-list");
  list.innerHTML = events.map(e => `<li>${e.title} (${e.status})</li>`).join("");
  fetchSwappable();
}

async function fetchSwappable() {
  const res = await fetch(`${API_BASE}/api/swappable-slots`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const slots = await res.json();
  const list = document.getElementById("swappable-list");
  list.innerHTML = slots.map(s => `<li>${s.title} (${s.owner_id})</li>`).join("");
}

