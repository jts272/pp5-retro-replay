function updateDeliveryCharge() {
  url = `${window.location.href}print/`;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      // AJAX delivery and grand total handling
      // Get elements
      const subtotalEl = document.getElementById("basket-subtotal");
      const deliveryEl = document.getElementById("delivery-charge");
      const totalEl = document.getElementById("grand-total");

      // Populate delivery charge with response data
      deliveryEl.innerText = Number(data["delivery charge"]);

      // Perform calculation to render grand total
      let grandTotal;
      const basketSubtotal = Number(subtotalEl.innerText);
      const deliveryCharge = Number(deliveryEl.innerText);
      grandTotal = (basketSubtotal + deliveryCharge).toFixed(2);
      totalEl.innerText = grandTotal;

      // Reload if all items are removed to render template guard clause
      if (basketSubtotal === 0) {
        location.reload();
      }
    });
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
