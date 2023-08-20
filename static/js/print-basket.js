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
      const incentiveEl = document.getElementById("delivery-incentive");

      // Populate delivery charge with response data
      deliveryEl.innerText = Number(data["delivery charge"]);

      // Perform calculation to render grand total
      let grandTotal;
      const basketSubtotal = Number(subtotalEl.innerText);
      const deliveryCharge = Number(deliveryEl.innerText);
      grandTotal = (basketSubtotal + deliveryCharge).toFixed(2);
      totalEl.innerText = grandTotal;

      // Calculate free delivery delta
      const deliveryIncentive = (FREE_DELIVERY_THRESHOLD - grandTotal).toFixed(
        2
      );

      // Alert classes are assigned or replaced dynamically
      incentiveEl.innerHTML = `Spend <strong>£${deliveryIncentive}</strong> more for free delivery.`;
      incentiveEl.classList.add("alert-info");
      incentiveEl.classList.replace("alert-success", "alert-info");

      if (grandTotal >= FREE_DELIVERY_THRESHOLD) {
        incentiveEl.innerHTML = `You have qualified for <strong>Free delivery!</strong>`;
        incentiveEl.classList.add("alert-success");
        incentiveEl.classList.replace("alert-info", "alert-success");
      }

      // Reload if all items are removed to render template guard clause
      if (basketSubtotal === 0) {
        location.reload();
      }
    });
}

// Invoke the fetching of the delivery charge
updateDeliveryCharge();

// Listen for DOM changes (i.e, item removed from basket)
// https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver#example
const basketContainer = document.getElementById("basket-container");
const targetNode = basketContainer;
const config = { attributes: true, childList: true, subtree: true };
// Create an observer instance linked to the callback function
const observer = new MutationObserver(updateDeliveryCharge);
// Start observing the target node for configured mutations
observer.observe(targetNode, config);
