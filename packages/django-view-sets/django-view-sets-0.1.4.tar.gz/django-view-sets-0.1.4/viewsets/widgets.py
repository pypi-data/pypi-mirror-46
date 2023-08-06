import copy
import json

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import (
    SELECT2_TRANSLATIONS, url_params_from_lookup_dict
)
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import get_language


class WidgetWrapper(forms.Widget):
    """
    This class is a wrapper to a given widget.
    """
    template_name = 'viewsets/widgets/wrapper.html'

    def __init__(self, widget):
        super().__init__(widget.attrs)
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.widget = widget

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    @property
    def choices(self):
        return self.widget.choices

    @choices.setter
    def choices(self, value):
        self.widget.choices = value

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def value_omitted_from_data(self, data, files, name):
        return self.widget.value_omitted_from_data(data, files, name)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)

    def get_context(self, name, value, attrs):
        context = self.widget.get_context(name, value, attrs)
        context['widget_template'] = self.widget.template_name
        return context

    @property
    def is_hidden(self):
        return self.widget.is_hidden

    @property
    def media(self):
        return self.widget.media


class UrlParametersMixin:
    def limit_parameters(self, rel):
        limit_choices_to = rel.limit_choices_to
        if callable(limit_choices_to):
            limit_choices_to = limit_choices_to()
        return url_params_from_lookup_dict(limit_choices_to)

    def get_parameters(self, rel):
        return self.limit_parameters(rel)

    def url_parameters(self, rel):
        params = self.get_parameters(rel)
        if not params:
            return ''
        return '?' + '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())


class RelatedWidgetWrapper(UrlParametersMixin, WidgetWrapper):
    template_name = 'viewsets/widgets/related_wrapper.html'

    def __init__(self, widget, add_related_url='', can_add_related=False):
        super().__init__(widget)
        self.add_related_url = add_related_url
        self.can_add_related = can_add_related

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        url = self.add_related_url
        rel = getattr(self.widget, 'rel', None)
        if rel:
            url += self.url_parameters(rel)
        context.update({
            'add_related_url': url,
            'can_add_related': self.can_add_related
        })
        return context


class LookupWidget(UrlParametersMixin, forms.TextInput):
    template_name = 'viewsets/widgets/lookup.html'

    def __init__(self, rel, list_url, obj_url_fn=None, attrs=None, using=None):
        self.rel = rel
        self.list_url = list_url
        self.obj_url_fn = obj_url_fn
        self.db = using
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        attrs['class'] = (attrs.get('class', '') + ' js-related-field').strip()
        context = super().get_context(name, value, attrs)
        context['related_url'] = mark_safe(self.list_url + self.url_parameters(self.rel))
        context['widget']['type'] = 'hidden'
        if context['widget']['value']:
            context['link_label'], context['link_url'] = self.label_and_url_for_value(value)
        return context

    def get_parameters(self, rel):
        from django.contrib.admin.views.main import TO_FIELD_VAR
        params = super().get_parameters(rel)
        params.update({TO_FIELD_VAR: self.rel.get_related_field().name})
        return params

    def label_and_url_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.model._default_manager.using(self.db).get(**{key: value})
        except (ValueError, self.rel.model.DoesNotExist, ValidationError):
            return '', ''

        url = ''
        if self.obj_url_fn:
            url = self.obj_url_fn(obj)

        return Truncator(obj).words(14, truncate='...'), url


class AutocompleteMixin(UrlParametersMixin):
    """
    Select widget mixin that loads options via AJAX.
    """

    def __init__(self, rel, url, attrs=None, choices=(), using=None):
        self.rel = rel
        self.url = url
        self.db = using
        self.choices = choices
        self.attrs = {} if attrs is None else attrs.copy()

    def build_attrs(self, base_attrs, extra_attrs=None):
        """
        Set select2's AJAX attributes.
        """
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault('class', '')
        attrs.update({
            'data-ajax--cache': 'true',
            'data-ajax--type': 'GET',
            'data-ajax--url': self.url,
            'data-theme': 'bootstrap4',
            'data-allow-clear': json.dumps(not self.is_required),
            'data-placeholder': '',  # Allows clearing of the input.
            'class': attrs['class'] + (' ' if attrs['class'] else '') + 'js-autocomplete',
            'data-params': json.dumps(self.get_parameters(self.rel)),
        })
        return attrs

    def optgroups(self, name, value, attr=None):
        """Return selected options based on the ModelChoiceIterator."""
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {
            str(v) for v in value
            if str(v) not in self.choices.field.empty_values
        }
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        choices = (
            (obj.pk, self.choices.field.label_from_instance(obj))
            for obj in self.choices.queryset.using(self.db).filter(pk__in=selected_choices)
        )
        for option_value, option_label in choices:
            selected = (str(option_value) in value and (has_selected is False or self.allow_multiple_selected))
            has_selected |= selected
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(name, option_value, option_label, selected_choices, index))
        return groups

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('viewsets/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=(
                'viewsets/js/vendor/select2/select2.full%s.js' % extra,
            ) + i18n_file + (
                'viewsets/js/autocomplete.js',
            ),
            css={
                'screen': (
                    'viewsets/css/vendor/select2/select2%s.css' % extra,
                    'viewsets/css/vendor/select2/select2-bootstrap4%s.css' % extra,
                ),
            },
        )


class AutocompleteWidget(AutocompleteMixin, forms.Select):
    pass


class AutocompleteManyWidget(AutocompleteWidget, forms.SelectMultiple):
    pass
