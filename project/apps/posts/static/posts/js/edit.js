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
    var ed;

    Footprints.post.editor.toggle_options = function() {
        $(".post_form").toggleClass("show_options");
        return false;
    };

    Footprints.post.editor.start_editing = function() {
        $(".edit_bar").addClass("editing");
        $(".post").addClass("editing");
        $(".post_form").addClass("editing");
        Footprints.post.editor.add_editors();
        
        return false;
    };
    Footprints.post.editor.add_editors = function() {
        Footprints.post.editor.editor_body = new Editor({
            element: $('#edit_body')[0],
            "status": false,
            "autofocus": false,
        });
        Footprints.post.editor.editor_title = new Editor({
            "element": "#edit_title",
            "toolbar": false,
            "status": false,
            "autofocus": false
        });
        Footprints.post.editor.editor_body.render();
        Footprints.post.editor.editor_title.render();
        $("body").click();
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
        console.log();
        console.log();

    };
    
    Footprints.post.actions.init = function() {
        $(".post_form").ajaxForm({
            dataType: 'json',
            beforeSerialize: function() {
                $("#id_title").val(Footprints.post.editor.editor_title.codemirror.getValue());
                $("#id_body").val(Footprints.post.editor.editor_body.codemirror.getValue());
            },
            success: function(json) {
                // Footprints.post.editor.cancel_editing();
                console.log(json)
                if (json.new_url) {
                document.location = json.new_url;
                }
            }
        });

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

        if (window.location.href.indexOf("?editing=true") != -1) {
            Footprints.post.editor.start_editing();
        }
        Dropzone.options.postImages = {
            url: Footprints.urls.upload_image,
            paramName: "file", // The name that will be used to transfer the file
            init: function() {
                this.on("success", function(file, resp) { 
                    var img = $("img", file.previewElement)
                    $(".all_images").append("<div><img src='"+img.attr("src")+"' class='list_thumb'><code>"+resp.url+"</code></div>")
                    console.log(file);
                    console.log(resp);
                });
            }

        };
    };
    Footprints.post.actions.init();

});
