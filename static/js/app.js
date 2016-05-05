/**
 * Returns django csrf token
 */
function getcsrf() {
    return (function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    })('csrftoken');
}


/**
 * Configure ajax requests
 */
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getcsrf());
        }
    }
});


/**
 * Instantiate plugins
 */
$(function () {
    // Dropdown plugin
    $('.dropdown').on('click', function () {
        $(this).toggleClass('active');
    });

    $('.dropdown ul').on('mouseleave', function () {
        $(this).parent().removeClass('active');
    });

    // Tokenize plugin
    $('.tokenize').each(function(i, e){
        var max = $(e).attr('data-max') || '';
        var src = $(e).attr('data-src') || '';
        var opt = {
            searchMinLength: 3
        };

        if ( max ) {
            opt['maxElements'] = parseInt(max);
        }

        if ( src ) {
            opt['datas'] = src;
        }

        return $(e).tokenize(opt);
    });

    // Autoresize event
    $('[data-autoresize]').on('keydown', function(){
        AutoResize(this, $(this).attr('data-autoresize'));
    });

    // Activate editor
    $('.editor:first-child').focus().keydown();
    $('.editor').on('keydown', function(){
        $(this).attr('contenteditable', 'true');
        if ( $(this).is('[data-empty]') ) {
            $(this).find('*').remove();
            $(this).removeAttr('data-empty');
        }
    });

    // Resize embed
    $(window).resize(function(){
        $('.embed.video').each(function(i, e){
            $(e).css('height', ($(e).width() / (16 / 9)) + 'px')
        });
    });

    $(window).resize();
});


/**
 * Resize with content
 * @param object
 * @param lh
 * @returns {*|jQuery}
 * @constructor
 */
function AutoResize(object, lh) {
    var lines = ($(object).val().split('\n') || $(object).html().split('<br>')).length + 1;
    var line_height = parseInt(lh || 24);
    return $(object).css({
        height: (lines * line_height) + 'px'
    });
}


/**
 * Public functionality
 * @type {{post: Public.post}}
 */
var Public = {
    post: function (input) {
        var val = ($(input).val() || $(input).html()).trim();
        if ( val.length > 1 && !$(input).is('[data-empty]') ) {
            $.ajax({
                url: document.location.pathname + '/post',
                method: 'post',
                data: {
                    content: $(input).val() || $(input).html()
                },
                dateType: 'html',
                success: function(response) {
                    $(input).val('');
                    $(input).html('');
                    $(input).keydown();
                    $('[data-fresh="entry"]').prepend(response).find('.empty').slideUp();
                }
            });
        }
    },
    comment: function (input, entry) {
        var val = ($(input).val() || $(input).html()).trim();
        if ( val.length > 1 && !$(input).is('[data-empty]') ) {
            $.ajax({
                url: '/feed/comment',
                method: 'post',
                data: {
                    target: entry,
                    content: $(input).val() || $(input).html()
                },
                dateType: 'html',
                success: function(response) {
                    $(input).val('');
                    $(input).html('');
                    $(input).keydown();
                    $('[data-fresh="comments"]').prepend(response).find('.empty').slideUp();
                }
            });
        }
    }
};


/**
 * Vote for an item
 * @param to
 * @param positive
 * @constructor
 */
var Vote = function(to, positive) {
    positive = parseInt(positive === undefined || positive == 1 ? 1 : 0);
    $.ajax({
        url: '/feed/vote',
        method: 'post',
        data: {
            to: to,
            positive: positive
        },
        success: function(response) {
            $('[data-target="' + to + '"]').text(response);
        }
    });
};
