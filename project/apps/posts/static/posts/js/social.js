$(function(){
    // Yes, I know this is circa-2008 style. I had no internet for a week when I wrote it and only jquery to write with.
    // Suck it. :)

    window.Footprints = window.Footprints || {};
    Footprints.share = {};
    Footprints.share.editor = {};
    Footprints.share.actions = {};
    Footprints.share.handlers = {};
    Footprints.share.state = {};

    Footprints.share.actions.show_hide_forms = function() {
        var hide_twitter = $("#id_twitter_publish_intent:checked").length == 0;
        $(".twitter_fields").toggleClass("disabled", hide_twitter);
        $(".twitter .include_image").toggleClass("disabled", hide_twitter);
        // $(".twitter .section_toggle").toggleClass("disabled", hide_twitter)
        if (hide_twitter) {
            $(".twitter_fields input, .twitter_fields textarea").attr("disabled", "disabled");
        } else {
            $(".twitter_fields input, .twitter_fields textarea").removeAttr("disabled");
        }
    
        if ($("#id_facebook_publish_intent:checked").length > 0) {
            $(".facebook_fields").removeClass("disabled");
            $(".facebook_fields input, .facebook_fields textarea").removeAttr("disabled");
        } else {
            $(".facebook_fields").addClass("disabled");
            $(".facebook_fields input, .facebook_fields textarea").attr("disabled", "disabled");
        }
    }
    Footprints.share.handlers.input_changed = function() {
        var num_remaining = 140-22-$(".twitter_fields textarea").val().length;
        $(".twitter .num_characters_remaining .number").html(num_remaining);
        $(".twitter .num_characters_remaining").toggleClass("over", num_remaining < 0)

        var num_remaining = 450-$(".facebook_fields textarea").val().length;
        $(".facebook .num_characters_remaining .number").html(Math.abs(num_remaining));
        $(".facebook .num_characters_remaining").toggleClass("over", num_remaining < 0)
        $(".facebook .num_characters_remaining .short").toggleClass("hidden", num_remaining<0)
        $(".facebook .num_characters_remaining .long").toggleClass("hidden", num_remaining>=0)
    }
    Footprints.share.actions.post_photo_twitter_changed = function() {
        var is_checked = $("#id_twitter_include_image:checked").length == 0;
        $(".twitter_fields .post_thumb").toggleClass("hidden", is_checked);
    }
    Footprints.share.actions.publish_now_changed = function() {
        var is_checked = $("#id_publish_now:checked").length > 0;
        if (is_checked) {
            // $(".sign_up_button").removeClass("btn-success").addClass("btn-primary");
            $(".sign_up_button").html("Publish Now")
        } else {
            // $(".sign_up_button").addClass("btn-success").removeClass("btn-primary");
            $(".sign_up_button").html("Save Changes and Publish Later")
        }
    }
    

    Footprints.share.actions.init = function() {
        $('.section_toggle input').on('switchChange.bootstrapSwitch', Footprints.share.actions.show_hide_forms);
        $(".twitter .include_image input").on('switchChange.bootstrapSwitch', Footprints.share.actions.post_photo_twitter_changed);
        $("#id_publish_now").on('switchChange.bootstrapSwitch', Footprints.share.actions.publish_now_changed);
        $(".twitter_fields textarea").keyup(Footprints.share.handlers.input_changed);
        $(".facebook_fields textarea").keyup(Footprints.share.handlers.input_changed);
        $(".facebook_fields textarea").autosize();
        

        $("input[type=checkbox]").bootstrapSwitch({
            "onText": "Yes",
            "offText": "No",
        });
        Footprints.share.actions.post_photo_twitter_changed();
        Footprints.share.actions.show_hide_forms();
        Footprints.share.handlers.input_changed();
        Footprints.share.actions.publish_now_changed();
    };
    Footprints.share.actions.init();

});
