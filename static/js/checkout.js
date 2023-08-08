const stripe = Stripe(
  "pk_test_51NMu8PEPb8OObKzZJEtyxn1AEAmJVbitHxGiYBMIOoVDEHgedK0qnuQexEHWPB3kbmS5C66CWj9uNtQCQRdTq9Px00oxNbOOdG"
);

const options = {
  // Fully customizable with appearance API.
  appearance: {
    /* ... */
  },
};

// Only need to create this if no elements group exist yet.
// Create a new Elements instance if needed, passing the
// optional appearance object.
const elements = stripe.elements(options);

// Create and mount the Address Element in shipping mode
const addressElement = elements.create("address", {
  mode: "shipping",
});
addressElement.mount("#address-element");
