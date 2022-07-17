let searchForm = $('#search-form');
let profileColLeft = $('#profile-col-left');
let indexColLeft = $('#index-col-left');

$(window).on('load resize', function () {
    if ($(window).width() < 768) {
        searchForm.addClass('input-group-sm');
        profileColLeft.removeClass('pe-0');
    } else if ($(window).width() > 768) {
        searchForm.removeClass('input-group-sm');
        profileColLeft.addClass('pe-0');
    };
});

$('#filter-view-toggle').on('click', function () {
    if (indexColLeft.hasClass('d-none')) {
        indexColLeft.addClass('d-block').removeClass('d-none');
    } else {
        indexColLeft.addClass('d-none').removeClass('d-block');
    };
});