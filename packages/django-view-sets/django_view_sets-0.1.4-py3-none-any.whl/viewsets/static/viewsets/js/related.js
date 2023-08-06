(function ($) {
  'use strict';

  function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
  }

  function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
  }

  function showRelatedPopup(link) {
    var href = link.href;
    href += (href.indexOf('?') === -1) ? '?_popup=1' : '&_popup=1';
    var width = Math.min(window.screen.width, 1000);
    var height = Math.min(window.screen.height, 500);
    var windowOptions = [
      'resizable=yes',
      'scrollbars=yes',
      `height=${height}`,
      `width=${width}`,
      `left=${Math.max((window.screen.width - width) / 2, 0)}`,
      `top=${Math.min((window.screen.height - height) / 2, 100)}`,
    ].join(',');
    var win = window.open(href, id_to_windowname(link.dataset['relatedFor']), windowOptions);
    win.focus();
    return false;
  }

  function setPopupValue(win, value, repr, url) {
    var input = $(`#${windowname_to_id(win.name)}`);
    if (input.is('select')) {
      if (!input.find(`option[value='${value}']`).length > 0) {
        input.append($('<option>', {
          value: value,
          text: repr,
        }));
      }
      if (input.prop('multiple')) {
        var new_val = input.val();
        new_val.push(value);
        input.val(new_val);
      } else {
        input.val(value);
      }
    } else {
      var repr_value = repr;
      if (url) {
        repr_value = '<a href="' + url + '" target="_blank">' + repr + '</a>';
      }
      input.data('related-repr', repr_value);
      input.val(value);
    }
    input.trigger('change');
    win.close();
  }

  function cleanToggle(field) {
    var clean = $(`[data-clean-for=${field.id}]`);
    if (!field.value) {
      clean.hide();
    } else {
      clean.show();
    }
  }

  window.setPopupValue = setPopupValue;

  $(function () {
    $('body').on('click', '.js-related-lookup', function (e) {
      e.preventDefault();
      showRelatedPopup(this);
    }).on('click', 'a[data-popup-value]', function (e) {
      e.preventDefault();
      opener.setPopupValue(window, this.dataset['popupValue'], this.dataset['popupRepr'], this.dataset['popupUrl']);
    }).on('change', '.js-related-field', function () {
      var $this = $(this);
      $(`#${this.id}_lookup_text`).html($this.data('related-repr'));
      cleanToggle(this);
    }).on('click', 'span[data-clean-for]', function () {
      var input = $(`#${this.dataset['cleanFor']}`);
      input.data('related-repr', '');
      input.val('').trigger('change');
    })
  });
})(jQuery);
