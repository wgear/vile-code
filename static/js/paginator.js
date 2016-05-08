/**
 * Lazy Paginator
 * @param resource
 * @param data
 * @constructor
 */
function Paginator(resource, data) {
    this.resource = resource;
    this.page = 1;
    this.start_data = data || {};
}


Paginator.prototype.load_next = function(btn) {
    var self = this;
    this.start_data.page = self.page + 1;
    $.ajax({
        url: self.resource,
        method: 'GET',
        data: self.start_data,
        success: function(response) {
            self.page += 1;
            $('[data-container]').append(response);
            $(btn).slideUp(300).delay(300).remove();
        }
    });
};