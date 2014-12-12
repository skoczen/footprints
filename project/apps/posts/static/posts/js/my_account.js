$(function() {
    var syncInterval = null;

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
        $(".find_dayone_folder").addClass('disabled');
        $(".find_dayone_folder .action_text").html("Finding....");
        $(".find_dayone_folder .icons").removeClass("hidden");
        $.ajax(window.Footprints.urls.find_dayone_folder, {
            success: dayone_success_response,
            failure: dayone_error_response,
        })
    });
    var check_sync_status = function() {
        $.ajax(window.Footprints.urls.sync_dayone_status, {
            success: function(resp){
                if (resp.success) {
                    if (resp.in_sync) {
                        extra_text = "";
                        if (!Footprints.status.ever_synced) {
                            extra_text = "<br/>This first sync can take a little while. Don't worry, you can leave, and come back later - it'll keep going!";
                        }
                        if (resp.current === 0) {
                            $(".sync_response_text").html("Getting list of posts..." + extra_text);
                        } else {
                            $(".sync_response_text").html(resp.current + "/" + resp.total + " posts synced." + extra_text);
                        }
                        setTimeout(check_sync_status, 500);
                    } else {
                        clearInterval(syncInterval);
                        $(".sync_icon i").removeClass("fa-spin");
                        $(".sync_response_text").html(resp.total + " posts synced from DayOne.");
                        $(".sync_status .current_status .timesince").html("Just now.")
                        $(".sync_status .current_status").show();
                        $(".sync_now_link .action_text").html("Sync again.");
                    }
                }
            }
        });
    }

    var sync_success_response = function(resp) {
        $(".sync_icon i").removeClass("fa-spin");
        if (resp.success == true) {
            check_sync_status();
        } else {
            $(".sync_response_text").html("Problem syncing!");
            $(".sync_now_link .action_text").html("Try again.");
        }
    };
    var sync_error_response = function() {
        $(".sync_icon i").removeClass("fa-spin");
        $(".sync_response_text").html("Unknown error. Sorry!");
        $(".sync_now_link .action_text").html("Try again.");
    };
    var show_sync_clicked = function() {
        $(".sync_now_link").addClass('disabled');
        $(".sync_status .current_status").hide();
        $(".sync_now_link .action_text").html("Syncing...");
        $(".sync_icon i").addClass("fa-spin");
        $(".sync_response_text").html("");

    }
    $(".sync_now_link").click(function(){
        show_sync_clicked();
        $.ajax(window.Footprints.urls.sync_dayone, {
            success: sync_success_response,
            failure: sync_error_response,
        })
    });

    if (Footprints.status.in_sync) {
        show_sync_clicked();
        check_sync_status();
    }
});