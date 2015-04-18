$(function(){
    var windowHeight = $(window).height();
    var imageHeight = windowHeight*0.8;
    $(".text_and_title").css({"margin-top": imageHeight});
    $(window).scrollTop(64);
    cheapoParallax();

    function cheapoParallax() {
        console.log("cheapoParallax")
        // Scroll about half of the way up.
        var scrollDistanceRatio = ($(window).scrollTop()/windowHeight);
        console.log(scrollDistanceRatio)
        if (scrollDistanceRatio < 1) {
            var new_top = scrollDistanceRatio * imageHeight * 0.4 * -1;
            console.log(new_top);
            $(".parallax_image").css({"top": new_top, "opacity": 1});
        } else {
            $(".parallax_image").css({"opacity": 0});
        }
    }
    $(window).scroll(cheapoParallax);
});
