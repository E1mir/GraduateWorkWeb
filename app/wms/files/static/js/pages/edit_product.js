'use strict';
var $modal = $("#editProduct"),
    $name = $("#editName"),
    $type = $("#editType"),
    $category = $("#category"),
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
    var $parent = $(this).parent().parent();
    var table_data = $parent.find("td");
    var description = $parent.find("div.sr-only").text();
    var name = table_data[1].innerText.trim(),
        type = table_data[2].innerText.trim(),
        category = table_data[3].innerText.trim(),
        price = table_data[5].innerText.trim(),
        count = table_data[6].innerText.trim();
    id_name = name;
    $name.val(name);
    $type.val(type);
    $category.val(category);
    $description.val(description);
    $price.val(price);
    $count.val(count);
});

$(document).on("click", "button.save-changes", function () {
    var update_object = {};
    update_object["name"] = $name.val();
    update_object["type"] = $type.val();
    update_object["category"] = $category.val();
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
