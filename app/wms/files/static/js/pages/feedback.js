var err = {};
$ajaxHover = $(".ajax-container");
$ajaxHover.hide();
$(document).ajaxStart(function () {
    $ajaxHover.show();
});
$(document).ajaxStop(function () {
    $ajaxHover.hide();
});
$("#sendMessage").on("click", function () {
    var feedbackData = {};
    var userName = $("#userName").val().trim(),
        userEmail = $("#userEmail").val().trim(),
        userSubject = $("#userSubject").val().trim(),
        userMessage = $("#userMessage").val().trim(),
        isValid = false;

    if (userName != "" && userEmail != "" && userSubject != "" && userMessage != "") {
        feedbackData["userName"] = userName;
        feedbackData["userEmail"] = userEmail;
        feedbackData["userSubject"] = userSubject;
        feedbackData["userMessage"] = userMessage;
        isValid = true;
    }
    if (isValid) {
        $.ajax({
            method: "POST",
            url: "/send",
            data: feedbackData,
            success: function (response) {
                swal({
                    title: "Successful",
                    text: "Your message was sent!",
                    type: "success",
                    confirmButtonText: "Go it!"
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
    } else {
        swal({
            title: "Fill all input data!",
            text: "",
            type: "warning",
            confirmButtonText: "Ok!"
        });
    }
});
console.log(err);