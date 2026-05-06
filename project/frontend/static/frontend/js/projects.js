const API_URL = "/api/projects/";
const TOKEN_URL = "/api/auth/token/";
const TOKEN_KEY = "portfolio_token";
const USERNAME_KEY = "portfolio_username";
const INDEX_URL = "/";
const LOGIN_URL = "/login/";
const CREATE_URL = "/projects/new/";

const getToken = () => localStorage.getItem(TOKEN_KEY);
const setToken = (t) => localStorage.setItem(TOKEN_KEY, t);
const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
};
const isAuthed = () => !!getToken();

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function setStatus(html) {
  const el = document.getElementById("status");
  if (el) el.innerHTML = html;
}

function clearOutput() {
  const el = document.getElementById("output");
  if (el) el.innerHTML = "";
}

function showElements(selector, visible) {
  document.querySelectorAll(selector).forEach((el) => {
    el.hidden = !visible;
  });
}

function updateAuthUI() {
  const authed = isAuthed();
  showElements(".anon-only", !authed);
  showElements(".auth-only", authed);
  const currentUser = document.getElementById("current-user");
  if (currentUser) currentUser.textContent = localStorage.getItem(USERNAME_KEY) || "";
}

async function apiFetch(url, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) headers["Authorization"] = `Token ${token}`;
  return fetch(url, { ...options, headers });
}

function formatErrors(data) {
  if (!data || typeof data !== "object") return "";
  return Object.entries(data)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`)
    .join("; ");
}

function projectRowHtml(p, authed) {
  const end = p.end_date ? p.end_date : "present";
  const actions = authed
    ? `<div class="project-actions">
         <button type="button" class="btn-secondary edit-btn" data-id="${p.id}">Edit</button>
         <button type="button" class="btn-danger delete-btn" data-id="${p.id}">Delete</button>
       </div>`
    : "";
  return `
    <div class="project-row" data-id="${p.id}">
      <div class="project-body">
        <h3>${escapeHtml(p.name)}</h3>
        <p>${escapeHtml(p.description)}</p>
        <p><strong>Technologies:</strong> ${escapeHtml(p.technologies)}</p>
        <p class="meta">${p.start_date} &mdash; ${end}</p>
      </div>
      ${actions}
    </div>`;
}

function projectEditorHtml(p) {
  return `
    <form class="project-edit" data-id="${p.id}">
      <label><span>Name</span><input name="name" value="${escapeHtml(p.name)}" required /></label>
      <label><span>Description</span><textarea name="description" rows="3" required>${escapeHtml(p.description)}</textarea></label>
      <label><span>Technologies</span><input name="technologies" value="${escapeHtml(p.technologies)}" required /></label>
      <label><span>Start date</span><input name="start_date" type="date" value="${p.start_date}" required /></label>
      <label><span>End date</span><input name="end_date" type="date" value="${p.end_date || ""}" /></label>
      <div class="project-actions">
        <button type="submit" class="btn-primary">Save</button>
        <button type="button" class="btn-secondary cancel-edit">Cancel</button>
      </div>
      <div class="error-banner" hidden></div>
    </form>`;
}

function renderProjects(results) {
  const output = document.getElementById("output");
  if (!output) return;
  if (!results || results.length === 0) {
    output.innerHTML = '<p class="empty-state">No projects found.</p>';
    return;
  }
  const authed = isAuthed();
  output.innerHTML = results.map((p) => projectRowHtml(p, authed)).join("");
}

async function fetchData() {
  setStatus('<span class="spinner" aria-label="Loading"></span>Loading projects…');
  clearOutput();
  try {
    const response = await apiFetch(API_URL);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const data = await response.json();
    setStatus("");
    renderProjects(data.results || data);
  } catch (err) {
    setStatus("");
    const output = document.getElementById("output");
    if (output) {
      output.innerHTML =
        `<div class="error-banner">Failed to load projects: ${escapeHtml(err.message)}</div>`;
    }
  }
}

async function login(username, password) {
  const errorBox = document.getElementById("login-error");
  if (errorBox) {
    errorBox.hidden = true;
    errorBox.textContent = "";
  }
  try {
    const response = await fetch(TOKEN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      const msg =
        (data.non_field_errors && data.non_field_errors[0]) ||
        formatErrors(data) ||
        `Login failed (${response.status})`;
      throw new Error(msg);
    }
    const data = await response.json();
    setToken(data.token);
    localStorage.setItem(USERNAME_KEY, username);
    window.location.href = INDEX_URL;
  } catch (err) {
    if (errorBox) {
      errorBox.textContent = err.message;
      errorBox.hidden = false;
    }
  }
}

function logout() {
  clearToken();
  updateAuthUI();
  clearOutput();
  setStatus("");
}

function setupCreatePage() {
  const form = document.getElementById("create-form");
  if (!form) return;
  if (!isAuthed()) {
    window.location.href = LOGIN_URL;
    return;
  }
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorBox = document.getElementById("create-error");
    errorBox.hidden = true;
    errorBox.textContent = "";
    const fd = new FormData(form);
    const payload = {
      name: fd.get("name"),
      description: fd.get("description"),
      technologies: fd.get("technologies"),
      start_date: fd.get("start_date"),
      end_date: fd.get("end_date") || null,
    };
    try {
      const response = await apiFetch(API_URL, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(formatErrors(data) || `Create failed (${response.status})`);
      }
      window.location.href = INDEX_URL;
    } catch (err) {
      errorBox.textContent = err.message;
      errorBox.hidden = false;
    }
  });
}

async function deleteProject(id) {
  if (!confirm("Delete this project?")) return;
  const response = await apiFetch(`${API_URL}${id}/`, { method: "DELETE" });
  if (!response.ok) {
    alert(`Delete failed (${response.status})`);
    return;
  }
  fetchData();
}

async function startEdit(id) {
  const row = document.querySelector(`.project-row[data-id="${id}"]`);
  if (!row) return;
  try {
    const response = await apiFetch(`${API_URL}${id}/`);
    if (!response.ok) throw new Error(`Could not load project (${response.status})`);
    const project = await response.json();
    row.outerHTML = projectEditorHtml(project);
  } catch (err) {
    alert(err.message);
  }
}

async function submitEdit(form) {
  const id = form.dataset.id;
  const errorBox = form.querySelector(".error-banner");
  errorBox.hidden = true;
  errorBox.textContent = "";
  const fd = new FormData(form);
  const payload = {
    name: fd.get("name"),
    description: fd.get("description"),
    technologies: fd.get("technologies"),
    start_date: fd.get("start_date"),
    end_date: fd.get("end_date") || null,
  };
  try {
    const response = await apiFetch(`${API_URL}${id}/`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(formatErrors(data) || `Update failed (${response.status})`);
    }
    fetchData();
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.hidden = false;
  }
}

function setupLoginPage() {
  const form = document.getElementById("login-form");
  if (!form) return;
  if (isAuthed()) {
    window.location.href = INDEX_URL;
    return;
  }
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;
    login(username, password);
  });
}

function setupIndexPage() {
  const fetchBtn = document.getElementById("fetch-btn");
  if (!fetchBtn) return;

  fetchBtn.addEventListener("click", fetchData);

  document.getElementById("logout-btn").addEventListener("click", logout);

  const output = document.getElementById("output");
  output.addEventListener("click", (e) => {
    if (e.target.matches(".edit-btn")) startEdit(e.target.dataset.id);
    else if (e.target.matches(".delete-btn")) deleteProject(e.target.dataset.id);
    else if (e.target.matches(".cancel-edit")) fetchData();
  });
  output.addEventListener("submit", (e) => {
    if (e.target.matches(".project-edit")) {
      e.preventDefault();
      submitEdit(e.target);
    }
  });
}

updateAuthUI();
setupLoginPage();
setupIndexPage();
setupCreatePage();
