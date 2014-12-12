$(function() {
    var dayone_success_response = function(resp) {
        console.log(resp)
        if (resp.success == true) {
            $(".dayone_response_text").html("Connected!");
        } else {
            $(".dayone_response_text").html("Couldn't find the DayOne folder. Have you set DayOne to sync using dropbox?");
        }
    };
    var dayone_error_response = function() {
        $(".dayone_response_text").html("Unknown error. Sorry!");
    };
    $(".find_dayone_folder.btn").click(function(){
        $(".find_dayone_folder").addClass('disabled').html("Finding....");
        $(".find_dayone_folder .icons").removeClass("hidden");
        $.ajax(window.Footprints.urls.find_dayone_folder, {

        }, dayone_success_response, dayone_error_response)
    });
});