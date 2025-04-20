function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle("dark");

  // Save preference
  const mode = body.classList.contains("dark") ? "dark" : "light";
  localStorage.setItem("mode", mode);
}

// Load preference on page load
window.onload = () => {
  if (localStorage.getItem("mode") === "dark") {
    document.body.classList.add("dark");
  }
};
