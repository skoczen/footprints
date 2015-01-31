$(function(){
    window.Footprints = window.Footprints || {};
    Footprints.post = {};
    Footprints.post.editor = {};
    Footprints.post.actions = {};
    Footprints.post.state = {};

    Footprints.post.toggle_prospect_success_response = function(resp) {
        if (resp.success) {
            $(".toggle_prospect[post_id=" + resp.pk + "]").toggleClass("is_prospect").toggleClass("on");
        }
    };
    Footprints.post.toggle_prospect_error_response = function(resp) {
        alert(resp);
    };
    Footprints.post.toggle_prospect = function() {
        var ele = $(this);
        $.ajax(ele.attr("href"), {
            success: Footprints.post.toggle_prospect_success_response,
            failure: Footprints.post.toggle_prospect_error_response,
        });
        return false;
    };
    
    Footprints.post.toggle_featured_success_response = function(resp) {
        if (resp.success) {
            $(".toggle_featured[post_id=" + resp.pk + "]").toggleClass("is_featured").toggleClass("on");
        }
    };
    Footprints.post.toggle_featured_error_response = function(resp) {
        alert(resp);
    };
    Footprints.post.toggle_featured = function() {
        var ele = $(this);
        $.ajax(ele.attr("href"), {
            success: Footprints.post.toggle_featured_success_response,
            failure: Footprints.post.toggle_featured_error_response,
        });
        return false;
    };
    
    Footprints.post.actions.init = function() {
        $(".toggle_prospect").click(Footprints.post.toggle_prospect);
        $(".toggle_featured").click(Footprints.post.toggle_featured);
    };
    Footprints.post.actions.init();

});
