$(function(){
    // Yes, I know this is circa-2008 style. I had no internet for a week when I wrote it and only jquery to write with.
    // Suck it. :)

    window.Footprints = window.Footprints || {};
    Footprints.post = {};
    Footprints.post.editor = {};
    Footprints.post.actions = {};
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
        Footprints.post.editor.add_editors();
        
        return false;
    };
    Footprints.post.editor.add_editors = function() {
        Footprints.post.editor.editor_body = new Editor({
            element: '#id_body',

        });
        // Footprints.post.editor.editor_title = new Editor({
        //     "element": "#title",
        //     "tools": false
        // });
        Footprints.post.editor.editor_body.render();
        // Footprints.post.editor.editor_title.render();

        // Footprints.post.editor.editing_node = new nicEditor({
        //         fullPanel : true,
        //         // buttonList : ['bold','italic','underline', 'blockquote', 'link']
        //         // Currently broke as fuck.  ,'left','center','right'
        // }).panelInstance("edit_pane", {hasPanel: true});
        // $(".post .editable").each(function(){
        //     id = $(this).attr("id");
        //     Footprints.post.editor.editing_node.addInstance(id, {hasPanel : true});
        //     Footprints.post.editor.editing_nodes[id] = ed;
        // });
        // $(".title .nicEdit-main").focus();
    };
    Footprints.post.editor.cancel_editing = function() {
        $(".edit_bar").removeClass("editing");
        $(".post").removeClass("editing");
        $(".post_form").removeClass("editing");
        $(".post_form").removeClass("show_options");
        // $(".revisions_button").show();
        Footprints.post.editor.remove_editors();
        return false;
    };
    Footprints.post.editor.remove_editors = function() {
        // $(".post .editable").each(function(){
        //     id = $(this).attr("id");
        //     var new_html = nicEditors.findEditor(id).getContent();
        //     $(this).html(new_html);
        // });
        // Footprints.post.editor.editing_node.removeInstance("edit_pane");
        // Footprints.post.editor.editing_node = null;
        // $("")
    };
    Footprints.post.toggle_fantastic = function() {
        var ele = $(this);
        ele.parents(".fantastic_form").submit();
    };
    Footprints.post.read_tracker.mark_read = function() {
        $(".read_form").submit();
    };
    Footprints.post.read_tracker.check_scroll = function() {
        if($(window).scrollTop() + $(window).height() > $(document).height() - 1110) {
            Footprints.post.read_tracker.saw_bottom = true;
            $(window).unbind("scroll.read");
            Footprints.post.read_tracker.mark_read_if_read();
            // $(".support").show();
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
        // seconds = 1000 * ((lines * 0.15) + (chars * 0.032));
        // seconds = 1000 * ((lines * 0.05) + (chars * 0.012));
        seconds = 1000 * 1.0 * chars / 6 / 300 * 60;

        return seconds;
    };
    Footprints.post.read_tracker.time_estimate = function() {
        var lines;
        var chars = $(".post .body").text().length;
        try {
            lines = $(".post .body").text().match(/\n/g).length;
        } catch (err) {
            lines = 0;
        }
        
        return Footprints.post.read_tracker.calculate_from_lines_and_chars(lines, chars);
    };

    Footprints.post.actions.init = function() {
        $(".post_form").ajaxForm({
            beforeSerialize: function() {
                // $("#id_title").val(nicEditors.findEditor("post_title").getContent());
                // $("#id_body").val(nicEditors.findEditor("post_body").getContent());
            },
            success: function(json) {
                Footprints.post.editor.cancel_editing();
                if (json.new_url) {
                    document.location = json.new_url;
                }
            }
        });
        if ($(".read_form").length > 0) {
            $(".read_form").ajaxForm({
                success: function(json) {
                    $(".num_reads .num").html(json.num_reads);
                }
            });
            $(window).on("scroll.read", Footprints.post.read_tracker.check_scroll);
            Footprints.post.read_tracker.check_scroll();
            setTimeout(Footprints.post.read_tracker.enough_time_callback, Footprints.post.read_tracker.time_estimate());
        }

        if ($(".fantastic_form").length > 0) {
            $(".fantastic_form").ajaxForm({
                beforeSerialize: function() {
                    $(".fantastic_button").toggleClass("clicked");
                    if ($(".fantastic_button").hasClass("clicked")) {
                        $("#id_on").val("True");
                    } else {
                        $("#id_on").val("False");
                    }
                },
                success: function(json) {
                    clearTimeout(Footprints.post.state.fantastic_timeout);
                    if (json.num_people > 1) {
                        $(".fantastic_button .num_agree .number").html(json.num_people).addClass("visible");
                        $(".fantastic_button .num_agree").addClass("visible");
                        Footprints.post.state.fantastic_timeout = setTimeout(function(){
                            $(".fantastic_button .num_agree").removeClass("visible");
                        }, 12000);
                    }
                }
            });
        }

        // Handlers
        // $(".save_revision_button").click(Footprints.post.actions.save_revision);
        $(".publish_button").click(function(){
            if (confirm("This will make your piece available to the general public.  There's no undo, but it is pretty awesome.  Ready to go?")) {
                $("#id_is_draft").val("False");
                $(".post_form").submit();
            }
            return false;
        });
        $(".start_editing_button").click(Footprints.post.editor.start_editing);
        $(".cancel_editing_button").click(Footprints.post.editor.cancel_editing);
        $(".options_button").click(Footprints.post.editor.toggle_options);
        $(".fantastic_button").click(Footprints.post.toggle_fantastic);

        if (window.location.href.indexOf("?editing=true") != -1) {
            Footprints.post.editor.start_editing();
        }
        hljs.initHighlightingOnLoad();
        // bkLib.onDomLoaded(nicEditors.allTextAreas);
    };
    Footprints.post.actions.init();

});
