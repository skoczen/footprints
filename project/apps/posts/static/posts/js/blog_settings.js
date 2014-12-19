$(function() {
    var update_header_preview = function() {
        $(".blog_header_preview").contents().find('html').html($("#id_blog_header").val());
    }
    $("#id_blog_header").change(update_header_preview);
    $("#id_blog_header").keyup(update_header_preview);

    var update_footer_preview = function() {
        $(".blog_footer_preview").contents().find('html').html($("#id_blog_footer").val());
    }
    $("#id_blog_footer").change(update_footer_preview);
    $("#id_blog_footer").keyup(update_footer_preview);
    update_header_preview()
    update_footer_preview()
});