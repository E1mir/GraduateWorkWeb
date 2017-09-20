var $modal = $("#editType"),
    $name = $("#editName"),
    $categories = $("#categories");
var $ajaxHover = $(".ajax-container");

$ajaxHover.hide();
$(document).ajaxStart(function () {
    $ajaxHover.show();
});
$(document).ajaxStop(function () {
    $ajaxHover.hide();
});

$(document).on("click", "button.edit-type", function () {
    var $parent = $(this).parents().eq(1),
        tableData = $parent.find("td");
    console.log(tableData);
    var name = tableData[1].innerText, categories = tableData[2].innerText;
    $name.val(name);
    $categories.val(categories);
});

$(".save-type").on("click", function () {
    String.prototype.capitalize = function () {
        return this.charAt(0).toUpperCase() + this.slice(1);
    };
    var editedData = {};
    var name = $name.val().trim();
    var categories = $categories.val().trim();
    if (name != "") editedData["name"] = name;
    else return;

    if (categories != "") {
        var categories_array = categories.split(",");
        var clean_array = [];
        for (var i = 0; i < categories_array.length; i++) {
            if (categories_array[i].trim() != "") {
                clean_array.push(categories_array[i].trim().capitalize());
            }
        }
        clean_array.sort();
        editedData["categories"] = clean_array.join(", ");
    }
    $modal.modal('hide');
    $.ajax({
        method: "POST",
        url: "/types/edit/" + name,
        data: editedData,
        success: function (response) {
            if (response != "Type name should be same or unique!!") {
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