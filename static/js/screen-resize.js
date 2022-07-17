$(window).on('load resize', function () {
    if ($(window).width() < 768) {
        $('#search-form').addClass('input-group-sm');
    } else if ($(window).width() > 768) {
        $('#search-form').removeClass('input-group-sm');
    };
});