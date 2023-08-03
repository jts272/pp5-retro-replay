// Reference: https://youtu.be/VOwfGW-ZTIY?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&t=7011

$(document).on("click", "#add-to-basket", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    // Connect to a URL, which is connected to a view
    url: null, // Must be added in inline script to utilize Django template tags
    data: {
      productId: $("add-to-basket").val(),
      csrfmiddlewaretoken: null, // Get inline from template
      action: "post",
    },
    // Data that is returned
    success: function (json) {},
    error: function (xhr, errmsg, err) {},
  });
});
