$(function () {
    $("single__pro").slice(0,16).show();
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $("single__pro:hidden").slice(0, 16).slideDown();
        if ($("single__pro:hidden").length == 0) {
            $("#load").fadeOut('slow');
        }
        $('html,body').animate({
            scrollTop: $(this).offset().top
        }, 1500);
    });
});

$('a[href=#top]').click(function () {
    $('body,html').animate({
        scrollTop: 0
    }, 600);
    return false;
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('.totop a').fadeIn();
    } else {
        $('.totop a').fadeOut();
    }
});