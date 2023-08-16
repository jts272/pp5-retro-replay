// Get the 'ask' and 'do' buttons on the page as iterables
const confirmDeleteBtns = Array.from(
  document.getElementsByClassName("delete-ask")
);
const actualDeleteBtns = Array.from(
  document.getElementsByClassName("delete-do")
);

// Iterate through each 'ask' button on the page
for (let i = 0; i < confirmDeleteBtns.length; i++) {
  const confirmBtn = confirmDeleteBtns[i];
  const deleteBtn = actualDeleteBtns[i];

  // Open the clicked 'ask' button to reveal the corresponding 'do' delete button
  confirmBtn.addEventListener("click", function (event) {
    deleteBtn.classList.toggle("visually-hidden");
  });
  confirmBtn.addEventListener("focusout", function (event) {
    deleteBtn.classList.add("visually-hidden");
  });
}
