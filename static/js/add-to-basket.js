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
