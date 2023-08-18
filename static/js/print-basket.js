function updateDeliveryCharge() {
  fetch("http://localhost:8000/basket/print/")
    .then((response) => response.json())
    .then((data) => console.log(data));
}

// Invoke the fetching of the delivery charge
updateDeliveryCharge();

// Test manual update the delivery charge by clicking a button
const updateBtn = document.getElementById("update-basket");
updateBtn.addEventListener("click", updateDeliveryCharge);

// Listen for DOM changes (i.e, item removed from basket)
// https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver#example
const basketContainer = document.getElementById("basket-container");
const targetNode = basketContainer;
const config = { attributes: true, childList: true, subtree: true };
// Create an observer instance linked to the callback function
const observer = new MutationObserver(updateDeliveryCharge);
// Start observing the target node for configured mutations
observer.observe(targetNode, config);
