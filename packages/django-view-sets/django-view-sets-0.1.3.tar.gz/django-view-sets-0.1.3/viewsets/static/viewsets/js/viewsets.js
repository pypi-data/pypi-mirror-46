$(function () {
  $('.js-order-link').on('click', function (e) {
    e.preventDefault();
    $('#filterForm input[name=o]').val($(this).data('order'));
    $('#filterForm').submit()
  });

  $('#collapseFilters').on('shown.bs.collapse hidden.bs.collapse', function () {
    var show = $('#collapseFilters').hasClass('show') ? true : '';
    document.cookie = "show_filters=" + show;
  });

  $(".formset").each(function () {
    var formset = $(this).formset('getOrCreate', {reorderMode: 'dom'});
    formset.$formset.on('formAdded', formset.opts.form, function () {
      var $form = $(this);
      $form.find('.js-autocomplete').djangoAdminSelect2();
    })
  });
});
