// Set up Stripe with publishable key
const stripe = Stripe(
  "pk_test_51NMu8PEPb8OObKzZJEtyxn1AEAmJVbitHxGiYBMIOoVDEHgedK0qnuQexEHWPB3kbmS5C66CWj9uNtQCQRdTq9Px00oxNbOOdG"
);

// Get client secret from the payment intent created in the checkout view
const payBtn = document.getElementById("pay-btn");
const clientSecret = payBtn.getAttribute("data-stripe-client-secret");

// Set up Stripe.js Elements, using the client secret
const elements = stripe.elements({ clientSecret: clientSecret });

// Get customer's address data if present
let addressObjectParsed;
const form = document.getElementById("payment-form");
const value = form.getAttribute("data-address-object");

if (value !== "None") {
  let addressObjectJson = form.dataset.addressObject;
  // Convert JSON returned from the view to an object
  addressObjectParsed = JSON.parse(addressObjectJson);
}

// Create and mount the Address Element in shipping mode
const addressElement = elements.create("address", {
  mode: "shipping",
  allowedCountries: ["gb"],
  autocomplete: { mode: "automatic" },

  // Fill address element with customer's saved address if present
  defaultValues: addressObjectParsed,
});
addressElement.mount("#address-element");

// Create and mount the Payment Element
const paymentElement = elements.create("payment");
paymentElement.mount("#payment-element");

// Submit the payment to Stripe
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  // Get loader and toggle visibility when submitted
  const loader = document.querySelector("#pacman-loader");
  loader.classList.toggle("d-none");
  // Update status on button text
  const payBtn = document.querySelector("#pay-btn-text");
  payBtn.textContent = "Processing...";

  const returnUrl = form.getAttribute("data-return-url");

  const { error } = await stripe.confirmPayment({
    //`Elements` instance that was used to create the Payment Element
    elements,
    confirmParams: {
      // Requires absolute url path - Django relative urls are not valid
      // Reference: https://css-tricks.com/snippets/javascript/get-url-and-url-parts-in-javascript/
      return_url: `${window.location.protocol}//${window.location.host}${returnUrl}`,
    },
  });

  if (error) {
    // This point will only be reached if there is an immediate error when
    // confirming the payment. Show error to your customer (for example, payment
    // details incomplete)
    const messageContainer = document.querySelector("#error-message");
    messageContainer.textContent = error.message;
    messageContainer.classList.add("alert", "alert-danger");

    // Toggle loader visibility that would have been added on submit
    loader.classList.toggle("d-none");
    // Update status on button text
    payBtn.textContent = "Retry payment";
  } else {
    // Your customer will be redirected to your `return_url`. For some payment
    // methods like iDEAL, your customer will be redirected to an intermediate
    // site first to authorize the payment, then redirected to the `return_url`.
  }
});
