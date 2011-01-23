(function($) {
  "use strict";

  var methods = {
    init: function(options) {
      var settings = $.extend({}, options);

      return this.each(function() {
        var $this = $(this),
            data = $this.data('editable'),

            editlink = $('<a />', {
              href: 'javascript:void(null);',
              class: 'edit',
              text: 'Edit'
            }),

            savelink = $('<input>', {
              type: 'submit',
              value: 'Save',
              class: 'link-button save',
              style: 'display: none'
            }),
            
            cancellink = $('<a />', {
              href: 'javascript:void(null);',
              class: 'cancel',
              text: 'Cancel',
              style: 'display: none'
            }),
            
            content = $this.find('.content'),
            textarea = $this.find('textarea');

        textarea.hide();

        if (!data) {
          editlink.click(function() {
            content.hide();
            editlink.hide();
            savelink.show();
            cancellink.show();
            textarea.css('display', 'block');
          });

          function reset() {
            textarea.hide();
            content.show();
            editlink.show();
            savelink.hide();
            cancellink.hide();
          }

          cancellink.click(reset);
          savelink.click(function() {
            var form = $this.find('form');
            $.ajax({
              type: 'PUT',
              url: form.attr('action'),
              data: form.serialize(),
              success: function(data, status, xhr) {
                content.html(data.html);
                reset();
              }
            });

            return false;
          });

          content.before(editlink);
          content.before(savelink);
          content.before(cancellink);
          content.before($('<input>', {
            type: 'hidden',
            name: 'method',
            value: 'put'
          }));


          $this.wrapInner($('<form>', {
            method: 'post',
            action: settings.saveAction.replace('_id_', $this.attr('id'))
          }));

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
