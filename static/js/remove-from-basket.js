$(document).on("click", ".remove-from-basket", function (e) {
  e.preventDefault();
  // The div to be removed when the user removes an item from their basket
  // The div is given the same data attribute and value as the remove button
  const divToRemove = $(this).data("removal-index");
  $.ajax({
    type: "POST",
    // Connect to a URL, which is connected to a view
    url: document.getElementById("remove-from-basket").dataset.url,
    data: {
      productId: $(this).data("removal-index"),
      csrfmiddlewaretoken: document.querySelector("[name=csrfmiddlewaretoken]")
        .value,
      // Action that can be tested for type of request
      action: "post",
    },
    // Data is returned into the success function argument
    success: function (json) {
      // Update basket quantity counter without refreshing the page
      document.getElementById("basket-qty").innerText = json["basket quantity"];
      // Remove the div that contains the basket item
      $(
        ".basket-single-item[data-removal-index='" + divToRemove + "']"
      ).remove();
      // Update basket subtotal
      document.getElementById("basket-subtotal").innerText =
        json["basket subtotal"];
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
