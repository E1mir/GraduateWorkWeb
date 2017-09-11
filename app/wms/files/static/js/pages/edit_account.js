'use strict';
// var $initHTML = $("#editAccount");
var $modal = $(".modal");
var $ajaxHover = $(".ajax-container");

$ajaxHover.hide();
$(document).ajaxStart(function () {
    $ajaxHover.show();
});
$(document).ajaxStop(function () {
    $ajaxHover.hide();
});
var $username = $("#username"),
    $email = $("#email"),
    $type = $("select[name='type']"),
    $permission = $("select[name='permission']"),
    $balance = $("input[name='balance']"),
    $password = $("input[name='password']");

$(document).on("click", "button.edit-account", function () {
    var $parent = $(this).parents().eq(1);
    var table_data = $parent.find("td");
    var username = table_data[1].innerText.trim(),
        email = table_data[2].innerText.trim(),
        type = table_data[3].innerText.trim(),
        permission = table_data[4].innerText.trim(),
        balance = table_data[5].innerText.trim(),
        password = table_data[6].innerText.trim();

    $username.text(username);
    $email.text(email);
    balance = Number(balance);
    $type.val(type);
    $permission.val(permission);
    $balance.val(balance);
    $password.val(password);
});

$(document).on("click", "button.save-changes", function () {
    var update_object = {};
    var username = $username.text();
    update_object["username"] = username;
    update_object["email"] = $email.text();
    update_object["type"] = $type.val();
    update_object["permission"] = $permission.val();
    update_object["balance"] = $balance.val();
    update_object["password"] = $password.val();
    $modal.modal('hide');
    $.ajax({
        method: "POST",
        url: "/users/edit/" + username,
        data: update_object,
        success: function (response) {
            swal({
                title: "Account edited!",
                text: "Update page",
                type: "success",
                confirmButtonText: "Ok"
            });
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
