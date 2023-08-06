(function ($) {
  'use strict';
  var init = function ($element, options) {
    var el_params = $element.data('params');
    var settings = $.extend({
      ajax: {
        data: function (params) {
          return $.extend(el_params, {
            q: params.term,
            page: params.page,
            as: 'json',
          });
        }
      }
    }, options);
    $element.select2(settings);
    $element.on('change', '')
  };

  $.fn.djangoAdminSelect2 = function (options) {
    var settings = $.extend({}, options);
    $.each(this, function (i, element) {
      var $element = $(element);
      init($element, settings);
    });
    return this;
  };

  $(function () {
    // Initialize all autocompvare widgets except the one in the template
    // form used when a new formset is added.
    $('.js-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();
    // Fix open dropdown on clear and remove element.
    $('body').on('select2:unselecting', function () {
      $(this).data('unselecting', true);
    }).on('select2:opening', function (e) {
      if ($(this).data('unselecting')) {
        $(this).removeData('unselecting');
        e.preventDefault();
      }
    });
  });
}(jQuery));
