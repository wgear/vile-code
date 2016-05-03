$(function(){
    $.fn.droplet = function (option) {
        var self = $(this);
        var opt = $.extend({
            items: {},
            change: function () {},
            default: self.attr('data-value') || null,
            label: 'select',
            input: ''
        }, option);


        var droplet = {
            update_input: function (val) {
                if ( opt.input ) {
                    $(opt.input).val(val);
                }
            },
            render_lable: function () {
                var value = self.attr('data-value') || opt.default,
                    label = opt.items[value] || opt.label;

                self.find('span').remove();
                self.append('<span>' + label + '</span>');
                droplet.update_input(value);
            },
            attach_events: function () {
                self.find('li[data-value]').on('click', function () {
                    self.find('span, ul').remove();
                    self.find('li[data-value].active').removeClass('active');
                    self.attr('data-value', $(this).attr('data-value'));
                    $(this).addClass('active');
                    opt.change(self.attr('data-value'));
                    droplet.update_input(self.attr('data-value'));
                    droplet.render();
                });
            },
            render: function () {
                // Add class
                self.addClass('droplet');

                // Render lable
                this.render_lable();

                // Render items
                var list = $('<ul></ul>');
                $.each(opt.items, function (k, v) {
                    list.append('<li data-value="' + k + '">' + v + '</li>');
                });

                self.append(list);

                // Events
                this.attach_events();
            }
        };
        
        droplet.render();        
        return self;
    }
});