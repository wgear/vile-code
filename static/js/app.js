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
});