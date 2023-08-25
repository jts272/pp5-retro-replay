// Simulate clicking message close buttons after four seconds
const closeBtns = Array.from(document.getElementsByClassName("btn-close"));

closeBtns.forEach((i) => {
  setTimeout(() => i.click(), 4000);
});
