'use strict';
var $modal = $(".modal"),
    $name = $("#editName"),
    $type = $("#editType"),
    $description = $("#description"),
    $price = $("#editPrice"),
    $count = $("#count"),
    id_name;
var $ajaxHover = $(".ajax-container");

$ajaxHover.hide();
$(document).ajaxStart(function () {
    $ajaxHover.show();
});
$(document).ajaxStop(function () {
    $ajaxHover.hide();
});
$(document).on("click", "button.edit-product", function () {
    var $parent = $(this).parents().eq(1);
    var table_data = $parent.find("td");
    var name = table_data[1].innerText.trim(),
        type = table_data[2].innerText.trim(),
        description = table_data[3].innerText.trim(),
        price = table_data[4].innerText.trim(),
        count = table_data[5].innerText.trim();
    id_name = name;
    $name.val(name);
    $type.val(type);
    $description.val(description);
    $price.val(price);
    $count.val(count);
});

$(document).on("click", "button.save-changes", function () {
    var update_object = {};
    update_object["name"] = $name.val();
    update_object["type"] = $type.val();
    update_object["description"] = $description.val();
    update_object["price"] = $price.val();
    update_object["count"] = $count.val();
    $modal.modal('hide');
    $.ajax({
        method: "POST",
        url: "/goods/edit/" + id_name,
        data: update_object,
        success: function (response) {
            if (response != "Product name should be same or unique!!") {
                $(".table-responsive").html(response);
                swal({
                    title: "Product edited!",
                    text: "",
                    type: "success",
                    confirmButtonText: "Ok"
                });
            } else {
                swal({
                    title: "Error",
                    text: response,
                    type: "error",
                    confirmButtonColor: "#000",
                    confirmButtonText: "Ok!"
                });
            }
        },
        error: function (error) {
            swal({
                title: "Something went wrong!",
                text: "Error code: " + error.status + " " + error.statusText,
                type: "error",
                confirmButtonColor: "#000",
                confirmButtonText: "Ok!"
            });
        }
    });
});
