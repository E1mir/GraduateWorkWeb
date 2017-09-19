var $modal = $("#orderInfo").find(".modal-body");
var $ajaxHover = $(".ajax-container");

$ajaxHover.hide();
//noinspection JSUnresolvedFunction
$(document).ajaxStart(function () {
    $ajaxHover.show();
});

//noinspection JSUnresolvedFunction
$(document).ajaxStop(function () {
    $ajaxHover.hide();
});
$(document).on("click", "button.order-info", function () {
    $modal.html("");
    var $parent = $(this).parent();
    var productNames = $parent.find(".product-name");
    var countInfo = $parent.find(".count-info");
    for (var i = 0; i < productNames.length; i++) {
        var name = productNames[i].innerText;
        var countData = countInfo[i].innerText.split("-");
        var selected = countData[0];
        var available = countData[1];
        $modal.append('<button class="btn btn-sm" style="margin: 8px"><span>' + name + '</span> <span class="badge badge-secondary">' + selected + '</span></button>');
    }
});
$(document).on("click", "button.btn-accept", function () {
    var $parent = $(this).parents().eq(1);
    var accept = {};
    var tableData = $parent.find("td");
    var orderID = Number(tableData[1].innerText);
    var timeStamp = Math.floor(Date.now() / 1000);
    accept["status"] = "Accepted";
    accept["timestamp"] = timeStamp;
    $.ajax({
        method: "POST",
        url: "/order_confirmation/" + orderID,
        data: accept,
        success: function (response) {
            $(".table-responsive").html(response);
            swal({
                title: "Accepted!",
                text: "Order accepted.",
                type: "success",
                confirmButtonText: "Ok"
            });
        },
        error: function (error) {
            swal({
                title: "ERROR!",
                text: "Error code: " + error.status + " " + error.statusText,
                type: "error",
                confirmButtonText: "Ok"
            });
        }
    })
});
$(document).on("click", "button.btn-decline", function () {
    var $parent = $(this).parents().eq(1);
    var decline = {};
    var tableData = $parent.find("td");
    var orderID = Number(tableData[1].innerText);
    var totalCost = Number(tableData[3].innerText);
    var username = tableData[2].innerText;
    var timeStamp = Math.floor(Date.now() / 1000) + 14400;
    var productNames = $parent.find(".product-name");
    var countInfo = $parent.find(".count-info");
    var products = [];
    for (var i = 0; i < productNames.length; i++) {
        var name = productNames[i].innerText;
        var countData = countInfo[i].innerText.split("-");
        var selected = Number(countData[0]);
        var available = Number(countData[1]);
        var count = selected + available;
        products.push({"name": name, "count": count})
    }
    decline["status"] = "Declined";
    decline["username"] = username;
    decline["timestamp"] = timeStamp;
    decline["products"] = JSON.stringify(products);
    decline["total_cost"] = totalCost;
    swal({
            title: "Are you sure?",
            text: "Your will not be able to accept this order!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn-danger",
            confirmButtonText: "Yes, decline it!",
            closeOnConfirm: false
        },
        function () {
            $.ajax({
                method: "POST",
                url: "/order_confirmation/" + orderID,
                data: decline,
                success: function (response) {
                    $(".table-responsive").html(response);
                    swal({
                        title: "Declined!",
                        text: "Order declined.",
                        type: "success",
                        confirmButtonText: "Ok"
                    });
                },
                error: function (error) {
                    swal({
                        title: "ERROR!",
                        text: "Error code: " + error.status + " " + error.statusText,
                        type: "error",
                        confirmButtonText: "Ok"
                    });
                }
            });
        });
});
