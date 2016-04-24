/**
 * Created by yanmingwang on 4/5/16.
 */

$(window).scroll(function() {
    if ($(".navbar").offset().top > 100) {
        $(".navbar").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});