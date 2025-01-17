// Existing JavaScript Code
fetch("./JSON/docs.json")
  .then((response) => response.json())
  .then((data) => {
    const languageList = document.getElementById("languageList");
    data.languages.forEach((lang) => {
      const listItem = document.createElement("li");
      listItem.textContent = lang.title;
      listItem.style.cursor = "pointer";
      listItem.onclick = () => loadContent(lang);
      languageList.appendChild(listItem);
    });

    // Populate FAQs
    populateFAQs(data.faqs || []);

    // Populate Community Contributions
    populateContributions(data.contributions || []);
  })
  .catch((error) => console.error("Error loading JSON data:", error));

// Load Selected Language Content
function loadContent(language) {
  document.getElementById("contentTitle").textContent = language.title;
  document.getElementById("contentDescription").textContent =
    language.description;
  document.getElementById("codeSnippet").textContent = language.code;

  document.getElementById("docLink").href = language.docs;
  document.getElementById("apiLink").href = language.api;
  document.getElementById("tutorialLink").href = language.tutorials;
}

// Populate FAQs section
function populateFAQs(faqs) {
  const faqSection = document.getElementById("faqSection");
  const faqList = faqSection.querySelector("ul");
  faqList.innerHTML = ""; // Clear existing content

  faqs.forEach((faq) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
      <strong>Q:</strong> ${faq.question} <br />
      <strong>A:</strong> ${faq.answer}
    `;
    faqList.appendChild(listItem);
  });
}

// Populate Community Contributions
function populateContributions(contributions) {
  const contributionsSection = document.getElementById(
    "communityContributions"
  );
  const contributionsList = contributionsSection.querySelector("ul");
  contributionsList.innerHTML = ""; // Clear existing content

  contributions.forEach((contributor) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${contributor.name} - ${contributor.snippets} snippets`;
    contributionsList.appendChild(listItem);
  });
}

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

