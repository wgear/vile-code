$(function () {
    $.fn.fixedHeight = function (height) {
        var self = this;
        var tool = {
            getLabel: function ($e) {
                return {
                    more: $e.attr('data-max') || 'more',
                    less: $e.attr('data-min') || 'less'
                }
            }
        };

        return this.each(function (i, e) {
            var $e = $(e);
            var label = tool.getLabel($e);
        });
    }
});
