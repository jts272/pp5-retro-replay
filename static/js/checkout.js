// Set up Stripe with publishable key
const stripe = Stripe(
  "pk_test_51NMu8PEPb8OObKzZJEtyxn1AEAmJVbitHxGiYBMIOoVDEHgedK0qnuQexEHWPB3kbmS5C66CWj9uNtQCQRdTq9Px00oxNbOOdG"
);

// Get client secret from the payment intent created in the checkout view
const payBtn = document.getElementById("pay-btn");
const clientSecret = payBtn.getAttribute("data-stripe-client-secret");

// Set up Stripe.js Elements, using the client secret
const elements = stripe.elements({ clientSecret: clientSecret });

// Create and mount the Address Element in shipping mode
const addressElement = elements.create("address", {
  mode: "shipping",
  allowedCountries: ["gb"],
});
addressElement.mount("#address-element");

// Create and mount the Payment Element
const paymentElement = elements.create("payment");
paymentElement.mount("#payment-element");
