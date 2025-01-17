document.addEventListener("DOMContentLoaded", () => {
  const profileButton = document.getElementById("profileDropdownButton");
  const profileContainer = document.querySelector(".profile-container");

  // Add click event to animate the gear icon
  profileContainer.addEventListener("click", () => {
    profileButton.classList.add("rotate-gear");

    // Remove the animation class after the animation completes
    setTimeout(() => {
      profileButton.classList.remove("rotate-gear");
    }, 1000); // Match this duration with the animation duration in CSS
  });
});

// Code Snippets for Each Aim
const codeSnippets = {
  python_tictactoe: `# Python - Tic Tac Toe
def print_board(board):
  for row in board:
      print(" | ".join(row))
      print("-" * 5)

board = [[" " for _ in range(3)] for _ in range(3)]
print_board(board)`,

  java_bfsdfs: `// Java - BFS & DFS
import java.util.*;

class Graph {
  private int V;
  private LinkedList<Integer>[] adj;

  Graph(int v) {
      V = v;
      adj = new LinkedList[v];
      for (int i = 0; i < v; i++)
          adj[i] = new LinkedList<>();
  }

  void BFS(int s) { /* BFS implementation */ }
  void DFS(int v) { /* DFS implementation */ }
}`,

  js_login: `// JavaScript - Simple Login Page
const users = { user1: "password123", user2: "mypassword" };

function login(username, password) {
  if (users[username] === password) {
      console.log("Login successful!");
  } else {
      console.log("Invalid credentials");
  }
}

login("user1", "password123");`,

  cpp_sorting: `// C++ - Sorting Algorithms
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
  vector<int> arr = {5, 2, 9, 1, 5, 6};
  sort(arr.begin(), arr.end());
  for (int i : arr) cout << i << " ";
  return 0;
}`,

  php_forms: `<?php
// PHP - Form Backend
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST['name'];
  echo "Hello, " . htmlspecialchars($name);
}
?>`,

  ts_todo: `// TypeScript - To-Do App
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

const tasks: Task[] = [];
function addTask(title: string) {
  tasks.push({ id: tasks.length + 1, title, completed: false });
}`,

  r_visualization: `# R - Data Visualization
library(ggplot2)
data(mpg)
ggplot(mpg, aes(x=cty, y=hwy)) + geom_point()`,

  dart_chat: `// Dart - Chat App Skeleton
class Message {
String sender;
String content;

Message(this.sender, this.content);
}

void main() {
var msg = Message("User1", "Hello!");
print("\${msg.sender}: \${msg.content}");
}`,

  bash_backup: `# Bash - Automate Backups
#!/bin/bash
src="/home/user/data"
dest="/backup/\$(date +%Y-%m-%d)"
mkdir -p $dest
cp -r $src $dest
echo "Backup completed!"`,
};

let snippetKeys = Object.keys(codeSnippets);
let currentIndex = 0;
let autoSwitchInterval;
let pauseTimeout;

// Function to display code in the terminal
function displayCode(key) {
  const terminal = document.getElementById("codeOutput");
  terminal.textContent = codeSnippets[key] || "Code not found.";
  highlightSidebar(key);
}

// Function to highlight the active sidebar item
function highlightSidebar(activeKey) {
  const sidebarLinks = document.querySelectorAll(".sidebar a");
  sidebarLinks.forEach((link) => {
    if (link.getAttribute("onclick").includes(activeKey)) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
}

// Auto-switching logic
function autoSwitchCode() {
  displayCode(snippetKeys[currentIndex]);
  currentIndex = (currentIndex + 1) % snippetKeys.length; // Cycle through keys
}

// Start auto-switching
function startAutoSwitch() {
  autoSwitchInterval = setInterval(autoSwitchCode, 2000);
}

// Stop auto-switching
function stopAutoSwitch() {
  clearInterval(autoSwitchInterval);
}

// Pause auto-switching for 5 seconds
function pauseAutoSwitch() {
  stopAutoSwitch();
  clearTimeout(pauseTimeout); // Clear any existing timeout
  pauseTimeout = setTimeout(startAutoSwitch, 5000); // Resume after 5 seconds
}

// Attach click event to sidebar links
document.querySelectorAll(".sidebar a").forEach((link) => {
  link.addEventListener("click", (event) => {
    const key = link.getAttribute("onclick").match(/'(.*?)'/)[1]; // Extract key from onclick
    displayCode(key);
    pauseAutoSwitch(); // Pause auto-switching
  });
});

document.getElementById("copyButton").addEventListener("click", () => {
  const codeOutput = document.getElementById("codeOutput").textContent;

  if (!codeOutput.trim()) {
    alert("No code to copy!");
    return;
  }

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard
      .writeText(codeOutput)
      .then(() => {
        showToast();
      })
      .catch((err) => {
        console.error("Failed to copy code: ", err);
        alert("Failed to copy code.");
      });
  } else {
    // Fallback method
    fallbackCopyText(codeOutput);
  }
});

function fallbackCopyText(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed"; // Prevent scrolling
  textarea.style.opacity = "0"; // Hide element
  document.body.appendChild(textarea);
  textarea.select();

  try {
    const successful = document.execCommand("copy");
    if (successful) {
      showToast();
    } else {
      alert("Failed to copy code using fallback.");
    }
  } catch (err) {
    console.error("Fallback copy failed: ", err);
    alert("Failed to copy code.");
  }

  document.body.removeChild(textarea);
}

function showToast() {
  const toast = document.getElementById("toast");
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

// Initialize auto-switching
startAutoSwitch();

document.addEventListener("DOMContentLoaded", () => {
  const profileButton = document.getElementById("profileDropdownButton");
  const dropdownMenu = document.getElementById("profileDropdown");
  const profileContainer = document.querySelector(".profile-container");

  // Toggle dropdown on click
  profileContainer.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });

  // Close dropdown if clicked outside
  document.addEventListener("click", (event) => {
    if (
      !profileContainer.contains(event.target) &&
      !dropdownMenu.contains(event.target)
    ) {
      dropdownMenu.classList.remove("show");
    }
  });
});

// Search Functionality

// Fetch the JSON data
fetch("../JSON/searchData.json")
  .then((response) => response.json())
  .then((data) => {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    // Handle input event
    searchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase();
      searchResults.innerHTML = "";

      if (query.trim() !== "") {
        const filteredItems = data.items.filter(
          (item) =>
            item.title.toLowerCase().includes(query) ||
            item.description.toLowerCase().includes(query)
        );

        if (filteredItems.length > 0) {
          const resultsList = document.createElement("ul");

          filteredItems.forEach((item) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
              <a href="${item.link}" target="_blank">${item.title}</a>
              <p>${item.description}</p>
            `;
            resultsList.appendChild(listItem);
          });

          searchResults.appendChild(resultsList);
          searchResults.style.display = "block";
        } else {
          searchResults.innerHTML = "<p>No results found.</p>";
          searchResults.style.display = "block";
        }
      } else {
        searchResults.style.display = "none";
      }
    });
  })
  .catch((error) => console.error("Error loading search data:", error));

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
