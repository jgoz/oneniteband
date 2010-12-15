(function($) {
  "use strict";

  var methods = {
    init: function(options) {
      var settings = $.extend({}, options);

      return this.each(function() {
        var $this = $(this),
            data = $this.data('editable'),
            editlink = $('<a />', {
              href : 'javascript:void(null);',
              text : 'Edit'
            });

        if (!data) {
          editlink.click(function() {
            $this.find('.content').hide();
            $this.find('.content').before($('<p>Testing 123</p>'));
          });

          $this.find('.content').prepend(editlink);

          $(this).data('editable', {
            target : $this,
            editlink : editlink
          });
        }
      });
    },

    destroy : function() {
      return this.each(function() {
        var $this = $(this),
            data = $this.data('editable');

        // Namespacing FTW
        $(window).unbind('.editable');
        data.editable.remove();
        $this.removeData('editable');
      })
    },

    show : function() {},
    hide : function() {},
    update : function(content) {}
  };

  $.fn.editable = function(method) {
    if (methods[method]) {
      return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    }
    else if (typeof method === 'object' || !method) {
      return methods.init.apply(this, arguments);
    }
    else {
      $.error('Method ' + method + ' does not exist on jQuery.editable');
    }    
  };
})( jQuery );
