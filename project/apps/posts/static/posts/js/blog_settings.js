$(function() {
    var update_preview = function() {
        // $(".blog_header_preview").html($("#id_blog_header").val());
    }
    $("#id_blog_header").change(update_preview);
    $("#id_blog_header").keyup(update_preview);

});