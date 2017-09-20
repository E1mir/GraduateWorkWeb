$modal = $("#showDescription");
$(document).on("click", "button.show-description", function () {
    var $body = $modal.find(".modal-body");
    var desc = $(this).parent().find("div.sr-only").text();
    $body.html("<pre class='item-modal-pre'>" + desc + "</pre>");
});