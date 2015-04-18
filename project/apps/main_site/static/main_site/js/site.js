$(function(){
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    var imageHeight;

    function cheapoParallax() {
        // Scroll about half of the way up.
        var scrollDistanceRatio = ($(window).scrollTop()/windowHeight);
        if (scrollDistanceRatio < 1) {
            var new_top = scrollDistanceRatio * imageHeight * 0.4 * -1;

            $(".parallax_image").css({"top": new_top, "opacity": 1});
        } else {
            $(".parallax_image").css({"opacity": 0});
        }
    }
    function cheapoParallaxSetup() {
        

        // alert(windowHeight + "," + windowWidth);
        if (windowWidth == 1024) {
            // iPad Landscape
            imageHeight = 550;
            // Just not figuring out why media queries are being a bitch tonight.
            $(".post .text_and_title").css({"padding-top": 20});
        } else {
            if (windowWidth == 568) {
                imageHeight = 360;
            } else {
                if (windowWidth > windowHeight) {
                    imageHeight = windowHeight*windowWidth / 1500;    
                } else {
                    imageHeight = windowHeight * 0.4;    
                }
            }
        }
        $(".single_post .text_and_title").css({"margin-top": imageHeight});
        // $(window).scrollTop(64);
        cheapoParallax();
        $(window).scroll(cheapoParallax);
    }
    if ($(".single_post .text_and_title").length > 0) {
        cheapoParallaxSetup();
        $(window).resize(cheapoParallaxSetup);
    }
});
