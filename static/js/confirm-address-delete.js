// Achieve autofocus effect on modal
// Adapted from https://getbootstrap.com/docs/5.3/components/modal/

const addressDeleteModal = document.getElementById("exampleModal");
const modalInputs = Array.from(document.getElementsByClassName("modal-input"));

for (let i = 0; i < modalInputs.length; i++) {
  const element = modalInputs[i];
  element.addEventListener("shown.bs.modal", () => {
    element.focus();
  });
}
