(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Trending row: scroll with the arrow buttons.
  const row = document.querySelector("[data-row]");
  if (row) {
    document.querySelectorAll("[data-row-nav]").forEach((button) => {
      button.addEventListener("click", () => {
        const direction = Number(button.dataset.rowNav);
        row.scrollBy({
          left: direction * row.clientWidth * 0.8,
          behavior: reduceMotion ? "auto" : "smooth",
        });
      });
    });
  }
})();
