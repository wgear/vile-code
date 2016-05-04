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
        AutoResize(this, $(this).attr('data-autoresize'), $(this).attr('data-wordcount'));
    });

    // Activate editor
    $('.editor').on('click', function(){
        $(this).attr('contenteditable', 'true');
        if ( $(this).is('[data-empty]') ) {
            $(this).find('*').remove();
            $(this).removeAttr('data-empty');
        }

        return $(this).focus();
    });
});


/**
 * Resize with content
 * @param object
 * @param lh
 * @returns {*|jQuery}
 * @constructor
 */
function AutoResize(object, lh, wc) {
    var lines = ($(object).html().split('<br>') || $(object).val().split('\n')).length + 1;
    var line_height = parseInt(lh || 24);
    var word_count = wc || null;

    if ( word_count ) {
        var tokens = ($(object).text() || $(object).val()).split(' '), words = [];
        tokens.forEach(function(i){
            var st = i.split('\n');
            for ( var k = 0; k < st.length; k++ ) {
                words.push(st[k]);
            }
        });
        var cnt = 0;
        for ( var i = 0; i < words.length; i++ ) {
            var w = words[i].trim(',. !?-:');
            if (w.length > 0) {
                cnt++;
            }
        }

        $(word_count).text($(word_count).attr('data-wc') + ' ' + cnt);
    }

    return $(object).css({
        height: (lines * line_height) + 'px'
    });
}


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
                    $('[data-fresh="entry"]').prepend(response);
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
