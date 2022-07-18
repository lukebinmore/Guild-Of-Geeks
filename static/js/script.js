let searchForm = $('#search-form');
let profileColLeft = $('#profile-col-left');
let postColLeft = $('#post-col-left');
let indexColLeft = $('#index-col-left');

$(window).on('load resize', function () {
    if ($(window).width() < 768) {
        searchForm.addClass('input-group-sm');
        profileColLeft.removeClass('pe-0');
        postColLeft.removeClass('pe-0');
    } else if ($(window).width() > 768) {
        searchForm.removeClass('input-group-sm');
        profileColLeft.addClass('pe-0');
        postColLeft.addClass('pe-0');
    };
});

$('#filter-view-toggle').on('click', function () {
    if (indexColLeft.hasClass('d-none')) {
        indexColLeft.addClass('d-block').removeClass('d-none');
    } else {
        indexColLeft.addClass('d-none').removeClass('d-block');
    };
});

$(document).ready(function () {
    $('.select2').select2({
        placeholder: 'Choose an Option*',
        tags: true
    });
});

setTimeout(function () {
    let alert = new bootstrap.Alert($('#user-alert'));
    alert.close();
}, 5000);

var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    offset: 'bottom-in-view',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        $('.loading').hide();
    }
});