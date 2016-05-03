$(function () {
    $('.dropdown').on('click', function () {
        $(this).toggleClass('active');
    });

    $('.dropdown ul').on('mouseleave', function () {
        $(this).parent().removeClass('active');
    });
});