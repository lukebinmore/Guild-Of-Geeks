/* Declaring variables. */
let searchForm = $('#search-form');
let profileColLeft = $('#profile-col-left');
let postColLeft = $('#post-col-left');
let indexColLeft = $('#index-col-left');
let contactColLeft = $('#contact-col-left');
let helpColLeft = $('#help-col-left');

$(window).on('load resize change', function () {
    /* Checks the windows width, and adds/removes classes to match size. */
    if ($(window).width() < 768) {
        searchForm.addClass('input-group-sm');
        profileColLeft.removeClass('pe-0');
        postColLeft.removeClass('pe-0');
        contactColLeft.removeClass('pe-0');
        helpColLeft.removeClass('pe-0');
    } else if ($(window).width() > 768) {
        searchForm.removeClass('input-group-sm');
        profileColLeft.addClass('pe-0');
        postColLeft.addClass('pe-0');
        contactColLeft.addClass('pe-0');
        helpColLeft.addClass('pe-0');
    }

    /* Alters the hight attribute of profile picture preview to match width. */
    $('.profile-picture-preview').attr('height', $('.profile-picture-preview').width());
});

/* Displays or hides the filters on smaller screens */
$('#filter-view-toggle').on('click', function () {
    if (indexColLeft.hasClass('d-none')) {
        indexColLeft.addClass('d-block').removeClass('d-none');
    } else {
        indexColLeft.addClass('d-none').removeClass('d-block');
    }
});

/* Specifics the class and attributes for Select2 elements. */
$(document).ready(function () {
    $('.select2').select2({
        placeholder: 'Choose an Option*',
        tags: true
    });
});

/* Sets the img source for the profile picture preview */
$(document).on('load change', '.profile-picture-upload', function () {
    const file = this.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function (e) {
            $('.profile-picture-preview').attr('src', e.target.result);
        };
        reader.readAsDataURL(file);
    }
});

/* Sets the timeout for the alert messages */
setTimeout(function () {
    let alert = new bootstrap.Alert($('#user-alert'));
    alert.close();
}, 3000);

/* Sets the waypoints for ifinite scroll pages */
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    offset: 'bottom-in-view',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        $('.loading').hide();
        htmx.process(document.body);
    }
});

/* Combines the search field into the filters form */
$('#filter-form').submit(function () {
    $('#search-form :input').not(':submit').clone().hide().appendTo('#filter-form');
});