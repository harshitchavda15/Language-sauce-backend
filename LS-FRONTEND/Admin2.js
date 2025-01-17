/**************************************************************
 * GLOBALS & MOCK DATA
 **************************************************************/
let currentUser = { username: "", role: "" };
let isDarkMode = false;

// Mock "active users" (including yourself)
let activeUsers = [
  { username: "alice", role: "admin" },
  { username: "bob", role: "editor" },
  { username: "charlie", role: "viewer" },
  { username: "david", role: "editor" },
  { username: "eve", role: "viewer" }
];

// In-memory "snippets"
let snippets = [
  {
    id: 1,
    title: "Hello World JS",
    language: "JavaScript",
    framework: "Vanilla",
    category: "Frontend",
    tags: ["intro", "beginner"],
    code: "console.log('Hello World');",
    explanation: "A simple hello world example in JS."
  },
  {
    id: 2,
    title: "Basic Express Server",
    language: "JavaScript",
    framework: "Express",
    category: "Backend",
    tags: ["express", "server", "node"],
    code: "const express = require('express');",
    explanation: "Boilerplate express code."
  },
  {
    id: 3,
    title: "Django Hello View",
    language: "Python",
    framework: "Django",
    category: "Backend",
    tags: ["django", "python"],
    code: "def hello(request): return HttpResponse('Hello, Django!')",
    explanation: "Simple Django view returning hello response."
  }
];

// Mock user list
let users = [
  { username: "alice", role: "admin" },
  { username: "bob", role: "editor" },
  { username: "charlie", role: "viewer" }
];

/**************************************************************
 * ON LOAD
 **************************************************************/
window.addEventListener("DOMContentLoaded", () => {
  // If we have separate pages, index.html won't have admin elements, so check first
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) {
    loginBtn.addEventListener("click", handleLogin);
  }

  // Admin panel elements
  const logoutBtn = document.getElementById("logoutBtn");
  const logoutBtn2 = document.getElementById("logoutBtn2");
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);
  if (logoutBtn2) logoutBtn2.addEventListener("click", handleLogout);

  // Dark mode toggle
  const darkToggle = document.getElementById("darkModeToggle");
  if (darkToggle) darkToggle.addEventListener("click", toggleDarkMode);

  // Navigation (top nav + sidebar)
  const navItems = document.querySelectorAll("[data-view]");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const view = item.getAttribute("data-view");
      showView(view);
    });
  });

  // Snippets interactions
  const addSnippetBtn = document.getElementById("addSnippetBtn");
  if (addSnippetBtn) addSnippetBtn.addEventListener("click", () => showSnippetModal(null));

  const snippetSearch = document.getElementById("snippetSearch");
  if (snippetSearch) snippetSearch.addEventListener("input", renderSnippets);

  const filterLanguage = document.getElementById("filterLanguage");
  const filterCategory = document.getElementById("filterCategory");
  const filterFramework = document.getElementById("filterFramework");
  [filterLanguage, filterCategory, filterFramework].forEach(sel => {
    if (sel) sel.addEventListener("change", renderSnippets);
  });

  // Snippet Bulk Delete
  const bulkDeleteBtn = document.getElementById("bulkDeleteBtn");
  if (bulkDeleteBtn) bulkDeleteBtn.addEventListener("click", handleBulkDelete);

  const selectAllCheckbox = document.getElementById("selectAllCheckbox");
  if (selectAllCheckbox) selectAllCheckbox.addEventListener("change", toggleSelectAll);

  // Export/Import
  const exportBtn = document.getElementById("exportSnippetsBtn");
  const importBtn = document.getElementById("importSnippetsBtn");
  const importFileInput = document.getElementById("importFileInput");
  if (exportBtn) exportBtn.addEventListener("click", handleExportSnippets);
  if (importBtn) importBtn.addEventListener("click", () => importFileInput.click());
  if (importFileInput) importFileInput.addEventListener("change", handleImportSnippets);

  // Snippet Modal
  const cancelSnippetBtn = document.getElementById("cancelSnippetBtn");
  const saveSnippetBtn = document.getElementById("saveSnippetBtn");
  if (cancelSnippetBtn) cancelSnippetBtn.addEventListener("click", closeSnippetModal);
  if (saveSnippetBtn) saveSnippetBtn.addEventListener("click", saveSnippet);

  const step1Btn = document.getElementById("step1Btn");
  const step2Btn = document.getElementById("step2Btn");
  if (step1Btn) step1Btn.addEventListener("click", () => goToStep(1));
  if (step2Btn) step2Btn.addEventListener("click", () => goToStep(2));

  const snippetCodeEl = document.getElementById("snippetCode");
  const codePreviewEl = document.getElementById("codePreview");
  if (snippetCodeEl) {
    snippetCodeEl.addEventListener("input", () => {
      codePreviewEl.textContent = snippetCodeEl.value;
    });
  }

  // Render user table
  renderUsers();

  // If we are on admin.html, no user is logged in yet by default
  // The admin panel is hidden, so do nothing special until login
});


/**************************************************************
 * LOGIN / LOGOUT
 **************************************************************/
function handleLogin() {
  const userInput = document.getElementById("loginUser").value.trim();
  const passInput = document.getElementById("loginPass").value.trim();

  if (!userInput || !passInput) {
    alert("Please enter username & password.");
    return;
  }

  // Mock: if the username has 'admin' in it => role=admin, otherwise editor
  const role = userInput.toLowerCase().includes("admin") ? "admin" : "editor";
  currentUser = { username: userInput, role };

  // Hide login screen, show admin panel
  document.getElementById("loginScreen").style.display = "none";
  document.getElementById("adminPanel").style.display = "block";

  // Initialize dashboard
  document.getElementById("userRole").textContent = role.toUpperCase();
  document.getElementById("activeUsersCount").textContent = activeUsers.length;
  document.getElementById("snippetCount").textContent = snippets.length;

  // Show default view
  showView("dashboard");
  buildChart();
  populateFilters();
  renderSnippets();
}

function handleLogout() {
  if (!confirm("Are you sure you want to logout?")) return;
  currentUser = { username: "", role: "" };
  // Hide admin panel, show login screen
  document.getElementById("adminPanel").style.display = "none";
  document.getElementById("loginScreen").style.display = "flex";
}


/**************************************************************
 * DARK MODE
 **************************************************************/
function toggleDarkMode() {
  isDarkMode = !isDarkMode;
  if (isDarkMode) {
    document.body.classList.add("dark-mode");
  } else {
    document.body.classList.remove("dark-mode");
  }
}


/**************************************************************
 * VIEW SWITCHING
 **************************************************************/
function showView(viewId) {
  const views = [
    "view-dashboard",
    "view-snippets",
    "view-categories",
    "view-users",
    "view-settings"
  ];
  views.forEach(v => {
    document.getElementById(v).style.display = "none";
  });
  document.getElementById(`view-${viewId}`).style.display = "block";
}


/**************************************************************
 * DASHBOARD CHART
 **************************************************************/
let myChartInstance = null;
function buildChart() {
  if (!document.getElementById("myChart")) return;

  // Count by language
  const languageCounts = {};
  snippets.forEach(snip => {
    languageCounts[snip.language] = (languageCounts[snip.language] || 0) + 1;
  });

  const labels = Object.keys(languageCounts);
  const data = Object.values(languageCounts);

  const ctx = document.getElementById("myChart").getContext("2d");
  if (myChartInstance) {
    myChartInstance.destroy();
  }
  myChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Snippets by Language",
          data,
          backgroundColor: ["#514bcc","#3e3ea9","#ffc107","#28a745","#17a2b8","#dc3545"]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}


/**************************************************************
 * SNIPPETS
 **************************************************************/
const pageSize = 3;
let currentPage = 1;

function renderSnippets() {
  const snippetTableBody = document.querySelector("#snippetTable tbody");
  if (!snippetTableBody) return;

  let filteredSnips = applySnippetFilters();

  // Pagination
  const totalPages = Math.ceil(filteredSnips.length / pageSize);
  if (currentPage > totalPages && totalPages > 0) {
    currentPage = totalPages;
  }
  const startIdx = (currentPage - 1) * pageSize;
  const endIdx = startIdx + pageSize;
  const pageData = filteredSnips.slice(startIdx, endIdx);

  // Render table
  snippetTableBody.innerHTML = "";
  pageData.forEach(snip => {
    const row = document.createElement("tr");

    // Checkbox
    const tdCheckbox = document.createElement("td");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "snippetCheckbox";
    checkbox.value = snip.id;
    tdCheckbox.appendChild(checkbox);

    const tdTitle = document.createElement("td");
    tdTitle.textContent = snip.title;

    const tdLang = document.createElement("td");
    tdLang.textContent = snip.language;

    const tdFrm = document.createElement("td");
    tdFrm.textContent = snip.framework;

    const tdCat = document.createElement("td");
    tdCat.textContent = snip.category;

    const tdActions = document.createElement("td");

    // Edit button if admin/editor
    if (currentUser.role === "admin" || currentUser.role === "editor") {
      const editBtn = document.createElement("button");
      editBtn.className = "editBtn";
      editBtn.textContent = "Edit";
      editBtn.addEventListener("click", () => showSnippetModal(snip.id));
      tdActions.appendChild(editBtn);

      // Delete button if admin
      if (currentUser.role === "admin") {
        const delBtn = document.createElement("button");
        delBtn.className = "deleteBtn";
        delBtn.textContent = "Delete";
        delBtn.addEventListener("click", () => deleteSnippet(snip.id));
        tdActions.appendChild(delBtn);
      }
    } else {
      tdActions.textContent = "Read-only";
    }

    row.appendChild(tdCheckbox);
    row.appendChild(tdTitle);
    row.appendChild(tdLang);
    row.appendChild(tdFrm);
    row.appendChild(tdCat);
    row.appendChild(tdActions);

    snippetTableBody.appendChild(row);
  });

  renderPagination(totalPages);
}

function applySnippetFilters() {
  const searchVal = (document.getElementById("snippetSearch")?.value || "").toLowerCase();
  const langVal = document.getElementById("filterLanguage")?.value;
  const catVal = document.getElementById("filterCategory")?.value;
  const frmVal = document.getElementById("filterFramework")?.value;

  return snippets.filter(snip => {
    let matches = true;

    // tag-based search (e.g. "tag:python")
    if (searchVal.startsWith("tag:")) {
      const tagQuery = searchVal.replace("tag:", "").trim();
      if (!snip.tags.includes(tagQuery)) {
        matches = false;
      }
    } else {
      // normal text search (title, code, tags)
      const bigStr = (snip.title + snip.code + snip.tags.join(" ")).toLowerCase();
      if (searchVal && !bigStr.includes(searchVal)) {
        matches = false;
      }
    }

    if (langVal && snip.language !== langVal) {
      matches = false;
    }
    if (catVal && snip.category !== catVal) {
      matches = false;
    }
    if (frmVal && snip.framework !== frmVal) {
      matches = false;
    }
    return matches;
  });
}

function populateFilters() {
  const langSelect = document.getElementById("filterLanguage");
  const catSelect = document.getElementById("filterCategory");
  const frmSelect = document.getElementById("filterFramework");
  if (!langSelect || !catSelect || !frmSelect) return;

  // Gather sets
  const langSet = new Set();
  const catSet = new Set();
  const frmSet = new Set();

  snippets.forEach(s => {
    langSet.add(s.language);
    catSet.add(s.category);
    frmSet.add(s.framework);
  });

  // Reset
  langSelect.innerHTML = `<option value="">All Languages</option>`;
  catSelect.innerHTML = `<option value="">All Categories</option>`;
  frmSelect.innerHTML = `<option value="">All Frameworks</option>`;

  langSet.forEach(l => {
    const opt = document.createElement("option");
    opt.value = l;
    opt.textContent = l;
    langSelect.appendChild(opt);
  });
  catSet.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    catSelect.appendChild(opt);
  });
  frmSet.forEach(f => {
    const opt = document.createElement("option");
    opt.value = f;
    opt.textContent = f;
    frmSelect.appendChild(opt);
  });
}

function renderPagination(totalPages) {
  const paginationDiv = document.getElementById("snippetPagination");
  if (!paginationDiv) return;

  paginationDiv.innerHTML = "";
  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      currentPage = i;
      renderSnippets();
    });
    paginationDiv.appendChild(btn);
  }
}

function showSnippetModal(editId) {
  document.getElementById("snippetOverlay").classList.add("show");
  goToStep(1);

  if (editId) {
    // Editing existing snippet
    const snip = snippets.find(s => s.id === editId);
    if (!snip) return;
    document.getElementById("modalTitle").textContent = "Edit Snippet";
    document.getElementById("snippetOverlay").dataset.editId = editId;

    document.getElementById("snippetTitle").value = snip.title;
    document.getElementById("snippetLanguage").value = snip.language;
    document.getElementById("snippetFramework").value = snip.framework;
    document.getElementById("snippetCategory").value = snip.category;
    document.getElementById("snippetTags").value = snip.tags.join(", ");
    document.getElementById("snippetCode").value = snip.code;
    document.getElementById("codePreview").textContent = snip.code;
    document.getElementById("snippetExplanation").value = snip.explanation;
  } else {
    // Adding new
    document.getElementById("modalTitle").textContent = "Add Snippet";
    delete document.getElementById("snippetOverlay").dataset.editId;

    document.getElementById("snippetTitle").value = "";
    document.getElementById("snippetLanguage").value = "";
    document.getElementById("snippetFramework").value = "";
    document.getElementById("snippetCategory").value = "";
    document.getElementById("snippetTags").value = "";
    document.getElementById("snippetCode").value = "";
    document.getElementById("codePreview").textContent = "";
    document.getElementById("snippetExplanation").value = "";
  }
}

function closeSnippetModal() {
  document.getElementById("snippetOverlay").classList.remove("show");
}

function saveSnippet() {
  const overlay = document.getElementById("snippetOverlay");
  const editId = overlay.dataset.editId;

  const title = document.getElementById("snippetTitle").value.trim();
  const language = document.getElementById("snippetLanguage").value.trim();
  const framework = document.getElementById("snippetFramework").value.trim();
  const category = document.getElementById("snippetCategory").value.trim();
  const tagsStr = document.getElementById("snippetTags").value.trim();
  const code = document.getElementById("snippetCode").value;
  const explanation = document.getElementById("snippetExplanation").value;

  // Basic validations
  if (!title || !language || !category) {
    alert("Title, Language, and Category are required.");
    return;
  }
  const tags = tagsStr ? tagsStr.split(",").map(t => t.trim()) : [];

  if (editId) {
    // Update
    let snip = snippets.find(s => s.id === parseInt(editId));
    if (snip) {
      snip.title = title;
      snip.language = language;
      snip.framework = framework;
      snip.category = category;
      snip.tags = tags;
      snip.code = code;
      snip.explanation = explanation;
    }
  } else {
    // Create new
    const newId = snippets.length ? Math.max(...snippets.map(s => s.id)) + 1 : 1;
    snippets.push({
      id: newId,
      title, language, framework, category, tags, code, explanation
    });
  }

  closeSnippetModal();
  populateFilters();
  renderSnippets();
  buildChart();
}

function deleteSnippet(id) {
  if (!confirm("Delete this snippet?")) return;
  snippets = snippets.filter(s => s.id !== id);
  populateFilters();
  renderSnippets();
  buildChart();
}

function handleBulkDelete() {
  if (currentUser.role !== "admin") {
    alert("Only admins can bulk delete!");
    return;
  }
  const checkboxes = document.querySelectorAll(".snippetCheckbox:checked");
  if (!checkboxes.length) {
    alert("No snippets selected.");
    return;
  }
  if (!confirm(`Delete ${checkboxes.length} snippet(s)?`)) return;

  const idsToDelete = Array.from(checkboxes).map(c => parseInt(c.value));
  snippets = snippets.filter(s => !idsToDelete.includes(s.id));
  populateFilters();
  renderSnippets();
  buildChart();
}

function toggleSelectAll() {
  const checked = this.checked;
  const checkboxes = document.querySelectorAll(".snippetCheckbox");
  checkboxes.forEach(cb => {
    cb.checked = checked;
  });
}

/**************************************************************
 * IMPORT / EXPORT
 **************************************************************/
function handleExportSnippets() {
  // Export current snippet list as JSON
  const dataStr = JSON.stringify(snippets, null, 2);
  const blob = new Blob([dataStr], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "snippets_export.json";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function handleImportSnippets(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = event => {
    try {
      const importedData = JSON.parse(event.target.result);
      if (!Array.isArray(importedData)) {
        alert("Invalid file format. Expected an array of snippets.");
        return;
      }
      // Merge or just replace—here we do a simple merge
      const startingId = snippets.length ? Math.max(...snippets.map(s => s.id)) + 1 : 1;
      importedData.forEach((imp, idx) => {
        // Assign a new ID
        imp.id = startingId + idx;
        snippets.push(imp);
      });
      alert("Snippets imported successfully!");
      populateFilters();
      renderSnippets();
      buildChart();
    } catch (err) {
      alert("Error parsing file: " + err.message);
    }
  };
  reader.readAsText(file);
  e.target.value = ""; // Clear file input
}

/**************************************************************
 * MODAL STEPS
 **************************************************************/
function goToStep(step) {
  document.getElementById("step1").style.display = step === 1 ? "block" : "none";
  document.getElementById("step2").style.display = step === 2 ? "block" : "none";
  document.getElementById("step1Btn").classList.toggle("active", step === 1);
  document.getElementById("step2Btn").classList.toggle("active", step === 2);
}

/**************************************************************
 * USERS PAGE
 **************************************************************/
function renderUsers() {
  const usersTableBody = document.querySelector("#usersTable tbody");
  if (!usersTableBody) return;

  usersTableBody.innerHTML = "";
  users.forEach(u => {
    const tr = document.createElement("tr");

    const tdName = document.createElement("td");
    tdName.textContent = u.username;

    const tdRole = document.createElement("td");
    tdRole.textContent = u.role;

    const tdActions = document.createElement("td");
    // Simple Edit, Delete
    // Could be limited to admin
    if (currentUser.role === "admin") {
      const editBtn = document.createElement("button");
      editBtn.className = "editBtn";
      editBtn.textContent = "Edit Role";
      editBtn.addEventListener("click", () => editUserRole(u.username));
      tdActions.appendChild(editBtn);

      const delBtn = document.createElement("button");
      delBtn.className = "deleteBtn";
      delBtn.textContent = "Delete";
      delBtn.addEventListener("click", () => deleteUser(u.username));
      tdActions.appendChild(delBtn);
    } else {
      tdActions.textContent = "Read-only";
    }

    tr.append(tdName, tdRole, tdActions);
    usersTableBody.appendChild(tr);
  });
}

function editUserRole(username) {
  const newRole = prompt("Enter new role (admin/editor/viewer) for " + username);
  if (!newRole) return;
  const userObj = users.find(u => u.username === username);
  if (userObj) {
    userObj.role = newRole.toLowerCase();
    alert("Role updated for " + username);
    renderUsers();
  }
}

function deleteUser(username) {
  if (!confirm("Delete user " + username + "?")) return;
  users = users.filter(u => u.username !== username);
  alert(username + " removed.");
  renderUsers();
}



document.addEventListener("DOMContentLoaded", () => {
  const themeSwitch = document.getElementById("checkbox");
  const currentTheme = localStorage.getItem("theme");

  // Apply saved theme on page load
  if (currentTheme) {
    document.documentElement.setAttribute("data-theme", currentTheme);
    themeSwitch.checked = currentTheme === "dark";
  }

  // Toggle theme
  themeSwitch.addEventListener("change", () => {
    const theme = themeSwitch.checked ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  });
});
