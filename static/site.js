"use strict";

// Normal links perform the language reload. JavaScript only dismisses the menu.
const languageMenu = document.getElementById("language-menu");

if (languageMenu) {
  document.addEventListener("click", (event) => {
    if (languageMenu.open && !languageMenu.contains(event.target)) {
      languageMenu.open = false;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && languageMenu.open) {
      languageMenu.open = false;
      languageMenu.querySelector("summary").focus();
    }
  });
}
