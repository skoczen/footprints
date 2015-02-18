$(function(){
    // Yes, I know this is circa-2008 style. I had no internet for a week when I wrote it and only jquery to write with.
    // Suck it. :)

    window.Footprints = window.Footprints || {};
    Footprints.post = {};
    Footprints.post.editor = {};
    Footprints.post.actions = {};
    Footprints.post.handlers = {};
    Footprints.post.state = {};
    Footprints.post.editor.editing_nodes = [];
    Footprints.post.editor.is_editing = false;
    Footprints.post.read_tracker = {};
    Footprints.post.read_tracker.saw_bottom = false;
    Footprints.post.read_tracker.stayed_long_enough = false;
    Footprints.post.state.title = "";
    Footprints.post.state.body = "";
    Footprints.post.state.fantastic_timeout = null;
    var ed;

    Footprints.post.editor.toggle_options = function() {
        $(".post_form").toggleClass("show_options");
        return false;
    };

    Footprints.post.editor.start_editing = function() {
        $(".edit_bar").addClass("editing");
        $(".post").addClass("editing");
        $(".post_form").addClass("editing");
        // $(".revisions_button").hide();
        Footprints.post.editor.add_nicedit_editors();
        return false;
    };
    Footprints.post.editor.add_nicedit_editors = function() {
        Footprints.post.editor.editing_node = new nicEditor({
                fullPanel : false,
                buttonList : ['bold','italic','underline', 'link',]
                // Currently broke as fuck.  ,'left','center','right'
        }).panelInstance("edit_pane", {hasPanel: true});
        $(".post .editable").each(function(){
            id = $(this).attr("id");
            Footprints.post.editor.editing_node.addInstance(id, {hasPanel : true});
            Footprints.post.editor.editing_nodes[id] = ed;
        });
        $(".title .nicEdit-main").focus();
    };
    Footprints.post.editor.cancel_editing = function() {
        $(".edit_bar").removeClass("editing");
        $(".post").removeClass("editing");
        $(".post_form").removeClass("editing");
        $(".post_form").removeClass("show_options");
        // $(".revisions_button").show();
        Footprints.post.editor.remove_nicedit_editors();
        return false;
    };
    Footprints.post.editor.remove_nicedit_editors = function() {
        $(".post .editable").each(function(){
            id = $(this).attr("id");
            var new_html = nicEditors.findEditor(id).getContent();
            $(this).html(new_html);
        });
        Footprints.post.editor.editing_node.removeInstance("edit_pane");
        Footprints.post.editor.editing_node = null;
    };
    Footprints.post.toggle_fantastic = function() {
        var ele = $(this);
        ele.parents(".fantastic_form").submit();
    };
    Footprints.post.read_tracker.mark_read = function() {
        $(".read_form").submit();
    };
    Footprints.post.read_tracker.check_scroll = function() {
        if($(window).scrollTop() + $(window).height() > $(document).height() - 1280) {
            // Footprints.post.read_tracker.saw_bottom = true;
            $(window).unbind("scroll");
            // Footprints.post.read_tracker.mark_read_if_read();
            // Load next posts.
            Footprints.post.actions.load_next_posts();
        }
    };
    Footprints.post.read_tracker.enough_time_callback = function() {
        Footprints.post.read_tracker.stayed_long_enough = true;
        Footprints.post.read_tracker.mark_read_if_read();
    };
    Footprints.post.read_tracker.mark_read_if_read = function() {
        if (Footprints.post.read_tracker.stayed_long_enough && Footprints.post.read_tracker.saw_bottom) {
            Footprints.post.read_tracker.mark_read();
        }
    };
    Footprints.post.read_tracker.calculate_from_lines_and_chars = function(lines, chars) {
        // seconds = (chars * .11693548387096774193) - (3.63089330024813895755 * lines);
        seconds = 1000 * ((lines * 0.05) + (chars * 0.012));
        return seconds;
    };
    Footprints.post.read_tracker.time_estimate = function() {
        var chars = $(".post .body").text().length;
        try {
            var lines = $(".post .body").text().match(/\n/g).length;
        } catch (err) {
            var lines = 0;
        }
        
        return Footprints.post.read_tracker.calculate_from_lines_and_chars(lines, chars);
    };
    Footprints.post.actions.load_next_posts = function() {
        $.ajax(Footprints.urls.load_next_posts, {
            "method": "GET",
            "data": {
                'last_timestamp': window.Footprints.state.last_timestamp
            },
            "success": Footprints.post.handlers.more_posts_loaded
        });
    };
    Footprints.post.handlers.more_posts_loaded = function(resp) {
        if (resp.success) {
            $(".posts").append(resp.html);
            if (resp.last_timestamp !== false) {
                Footprints.state.last_timestamp = resp.last_timestamp;
                $(window).scroll(Footprints.post.read_tracker.check_scroll);
                Footprints.post.read_tracker.check_scroll();
                $(".fantastic_form").ajaxForm({
                    success: Footprints.post.handlers.fantastic_form_callback
                });
            } else {
                $(".the_start").addClass("visible");
            }
        }
    };
    Footprints.post.handlers.fantastic_form_callback = function(json) {
        clearTimeout(Footprints.post.state.fantastic_timeout);
        if (json.num_people > 1) {
            $(".post_" + json.post_id + " .fantastic_button .num_agree .number").html(json.num_people);
            $(".post_" + json.post_id + " .fantastic_button .num_agree").addClass("visible");
            Footprints.post.state.fantastic_timeout = setTimeout(function(){
                $(".post_" + json.post_id + " .fantastic_button .num_agree").removeClass("visible");
            }, 8000);
        }
    };
    Footprints.post.actions.init = function() {
        $(".fantastic_form").on('click', '.fantastic_button', function(){
            var ele = $(this);
            ele.toggleClass("clicked");
            form = ele.parents("form");
            if (ele.hasClass("clicked")) {
                $("input[name=on]", form).val("True");
            } else {
                $("input[name=on]", form).val("False");
            }
            form.submit();
            return false;
        });
        if ($(".read_form").length > 0) {
            $(".read_form").ajaxForm({
                success: function(json) {
                    $(".num_reads .num").html(json.num_reads);
                }
            });
            setTimeout(Footprints.post.read_tracker.enough_time_callback, Footprints.post.read_tracker.time_estimate());
        }
        if ($(".fantastic_form").length > 0) {
            $(".fantastic_form").ajaxForm({
                success: Footprints.post.handlers.fantastic_form_callback
            });
        }
        $(window).scroll(Footprints.post.read_tracker.check_scroll);
        Footprints.post.read_tracker.check_scroll();
        // $(".fantastic_button").click(Footprints.post.toggle_fantastic);
        hljs.initHighlightingOnLoad();
    };
    Footprints.post.actions.init();

});
