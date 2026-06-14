document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("orderModal");
  const modalBody = document.getElementById("modal-body");
  const closeBtn = document.querySelector(".close");

  document.querySelectorAll(".order-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();

      const card = link.closest(".order-card");
      const hiddenData = card.querySelector(".order-data");

      modalBody.innerHTML = hiddenData.innerHTML;

      modal.style.display = "block";
    });
  });

  closeBtn.onclick = () => modal.style.display = "none";

  window.onclick = (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  };
});