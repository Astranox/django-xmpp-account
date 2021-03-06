function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/**
 * Code to insert Facebook SDK.
 */
var fb_loaded = false;
var load_facebook = function() {
    // This is the code provided by facebook to asynchronously load their SDK
    if (! fb_loaded) {
        var e = document.createElement('script'); e.async = true;
        e.src = document.location.protocol +
          '//connect.facebook.net/en_US/all.js#xfbml=1';
        document.getElementById('fb-root').appendChild(e);
    }
    fb_loaded = true;
};


$(document).ready(function() {
    $('a.social').on('click', function(event) {
        link = $(event.currentTarget);
        url = link.attr('href');
        width = link.attr('data-width');
        height = link.attr('data-height');
        window.open(url, 'newwindow', 'width=' + width + ', height=' + height);
        return false;
    });

    /* This is only displayed on the submit page of a registration confirmation. */
    $('#fb-page-modal').on('show.bs.modal', function(e) {
        load_facebook();
    });

    $('.js-captcha-refresh').click(function(){
        $form = $(this).parents('form');

        $.getJSON(captcha_refresh_url, {}, function(json) {
            // This should update your captcha image src and captcha hidden input
            $('#captcha-form-data img').attr('src', json.image_url);
            $('#captcha-form-data input[type="hidden"]').attr('value', json.key);
        });

        return false;
    });
});
