$(function() {
    var tableObj;

    var update_header_preview = function() {
        if ($("#id_blog_header").val() != "") {
            $(".blog_header_preview").contents().find('html').html($("#id_blog_header").val())
            $(".blog_header_preview").show();
        } else {
            $(".blog_header_preview").hide();
        }
    }

    var update_footer_preview = function() {
        if ($("#id_blog_footer").val() != "") {
            $(".blog_footer_preview").contents().find('html').html($("#id_blog_footer").val())
            $(".blog_footer_preview").show();
        } else {
            $(".blog_footer_preview").hide();
        }
    }
    var set_redirect_data = function() {
        $("#id_redirects").val(JSON.stringify({data: tableObj.getData()}));
    }

    var init = function() {
        update_header_preview();
        update_footer_preview();

        $("#id_blog_header").change(update_header_preview);
        $("#id_blog_header").keyup(update_header_preview);
        $("#id_blog_footer").change(update_footer_preview);
        $("#id_blog_footer").keyup(update_footer_preview);

        var container = document.getElementById('redirectTable');
        tableObj = new Handsontable(container,
        {
            data: Footprints.data.redirects,
            minSpareRows: 1,
            colHeaders: true,
            contextMenu: true,
            colHeaders: ["Old URL", "Footprints URL"],
            stretchH: 'all',
            width: "100%",
            afterChange: function (change, source) {
                if (source === 'loadData') {
                  return; //don't save this change
                }
                set_redirect_data();
            }
        });
        set_redirect_data();
        
    };
    init();
});