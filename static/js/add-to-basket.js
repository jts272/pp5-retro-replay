// Reference: https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=7011
$(document).on("click", "#add-to-basket", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    // Connect to a URL, which is connected to a view
    url: document.getElementById("add-to-basket").dataset.url,
    // Data to send to the view
    data: {
      productId: $("#add-to-basket").val(),
      csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0]
        .value,
      action: "post",
    },
    // Data is returned into the success function argument
    success: function (json) {
      // Update basket quantity counter without refreshing the page
      document.getElementById("basket-qty").innerText = json["basket quantity"];
    },
    // Alert error information if returned
    error: function (jqXHR, textStatus, errorThrown) {
      window.alert(`
        An error occurred:
        Error status: ${textStatus}
        Error thrown: ${errorThrown}
        Status code: ${jqXHR.status}`);
    },
  });
});

// Show message without using Django messages in the view
const msgContainer = document.getElementById("js-msg-container");
const alertEl = document.getElementById("alert");
const msgContent = document.getElementById("js-msg-content");
const addBtn = document.getElementById("add-to-basket");
const closeBtn = document.getElementById("js-msg-close-btn");
const basketWarningContainer = document.getElementById(
  "basket-warning-container"
);

// Check if item is in basket on page load
let inBasket = addBtn.dataset.inBasket;

addBtn.addEventListener("click", () => {
  msgContainer.classList.remove("d-none");
  alertEl.classList.remove("alert-light");
  alertEl.classList.add("alert-success");
  msgContent.innerHTML = `Item added to basket! <a href="/basket/" class="float-end">View Basket</a>`;
  // Give users time to click the link before auto-dismissing the message
  setTimeout(() => closeBtn.click(), 8000);

  // Adjust button content now that item is in basket
  addBtn.classList.replace("btn-success", "btn-secondary");
  addBtn.innerHTML = `In Basket <i class="bi bi-basket"></i>`;

  // Handle additional attempts to add to basket
  addBtn.dataset.inBasket = true;
  inBasket = addBtn.dataset.inBasket;

  if (inBasket) {
    addBtn.addEventListener("click", () => {
      basketWarningContainer.classList.remove("d-none");
      basketWarningContainer.scrollIntoView();
    });
  }
});
