from datetime import date, datetime

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.template.defaultfilters import yesno
from django.utils.formats import date_format
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import ugettext_lazy as _


__all__ = ['BaseSerializer', 'ViewSetSerializer']


class BaseSerializer:
    empty_values = ('', None)
    type_map = {
        bool: 'handle_bool',
        models.Model: 'handle_model',
        models.QuerySet: 'handle_qs',
        models.Manager: 'handle_manager',
        ImageFieldFile: 'handle_image_file',
        FieldFile: 'handle_file',
        datetime: 'handle_datetime',
        date: 'handle_date',
    }

    def __init__(self, object_list=None, instance=None, **kwargs):
        if object_list is None and instance is None:
            raise ValueError('Must define "object_list" or "instance".')
        self.object_list = object_list
        self.instance = instance
        if self.instance:
            self.model = self.instance.__class__
        else:
            self.model = object_list.model
        self.fields = kwargs.get('fields') or ()
        self.fields_names = kwargs.get('fields_names') or {}
        self.default_value = kwargs.get('default_value') or ''
        self.datetime_format = kwargs.get('datetime_format')
        self.date_format = kwargs.get('date_format')

    def __iter__(self):
        if self.instance:
            return self.serialize_instance()
        else:
            return self.serialize_list()

    def get_field_name(self, field):
        if field in self.fields_names:
            return self.fields_names[field]
        try:
            model_field = self.model._meta.get_field(field)
        except FieldDoesNotExist:
            return field
        if isinstance(model_field, ForeignObjectRel):
            related_model = model_field.related_model
            if model_field.one_to_many:
                return related_model._meta.verbose_name_plural
            return related_model._meta.verbose_name
        return model_field.verbose_name

    def get_field_value(self, obj, field):
        if hasattr(self, f'get_{field}_value'):
            return getattr(self, f'get_{field}_value')(obj)
        if hasattr(obj, f'get_{field}_display'):
            return getattr(obj, f'get_{field}_display')()
        return getattr(obj, field)

    def get_typed_value(self, obj, field):
        value = self.get_field_value(obj, field)
        if isinstance(value, str):
            return value
        for _type, handler in self.type_map.items():
            if isinstance(value, _type):
                value = getattr(self, handler)(obj, field, value)
                break
        if callable(value):
            value = value()
        return value

    def get_value(self, obj, field):
        value = self.get_typed_value(obj, field)
        if value in self.empty_values:
            value = self.default_value
        return value

    def serialize_instance(self):
        return ((self.get_field_name(field), self.get_value(self.instance, field)) for field in self.fields)

    def serialize_list(self):
        for obj in self.object_list:
            yield obj, [self.get_value(obj, field) for field in self.fields]

    def handle_model(self, obj, field, value):
        return str(value)

    def handle_qs(self, obj, field, value):
        return ', '.join(map(str, value))

    def handle_manager(self, obj, field, value):
        return self.handle_qs(obj, field, value.all())

    def handle_bool(self, obj, field, value):
        return yesno(value)

    def handle_file(self, obj, field, value):
        if value:
            return value.url

    def handle_image_file(self, obj, field, value):
        return self.handle_file(obj, field, value)

    def handle_datetime(self, obj, field, value):
        return date_format(value, self.datetime_format)

    def handle_date(self, obj, field, value):
        return date_format(value, self.date_format)


class ViewSetSerializer(BaseSerializer):
    def __init__(self, object_list=None, instance=None, **kwargs):
        super().__init__(object_list, instance, **kwargs)
        self.request = kwargs.get('request')
        self.model_viewset = kwargs.get('model_viewset')
        self.bool_as_icon = kwargs.get('bool_as_icon', False)
        self.order_fields = kwargs.get('order_fields') or ()
        self.is_popup = self.request.GET.get('_popup')
        if not self.fields:
            self.fields = ('__str__',)
            self.fields_names = {'__str__': _('Name')}

    def serialize_list(self):
        for obj in self.object_list:
            row = []
            for field in self.fields:
                value = self.get_value(obj, field)
                if value and not row:
                    value = self.get_obj_link(obj, text=str(obj) if field == '__str__' else value)
                row.append(value)
            yield obj, row

    @property
    def cols(self):
        return (
            (field, self.get_field_name(field), self.is_sortable(field))
            for field in self.fields
        )

    def is_sortable(self, field):
        return field in self.order_fields

    def get_model_viewset(self, obj):
        if obj.__class__ is self.model:
            return self.model_viewset
        if not self.model_viewset.viewset:
            return None
        return self.model_viewset.viewset.get_registered(obj.__class__)

    def get_obj_link(self, obj, text=None):
        text = text or str(obj)
        if not isinstance(text, SafeText):
            text = escape(text)

        model_viewset = self.get_model_viewset(obj)
        if not model_viewset:
            return text

        url = model_viewset.get_obj_url(self.request, obj)
        if not url and not self.is_popup:
            return text

        data = ''
        blank = (obj.__class__ is not self.model)
        if self.request.GET.get('_popup'):
            to_field = self.request.GET.get('_to_field') or 'pk'
            data = 'data-popup-value="{}" data-popup-repr="{}" data-popup-url="{}"'.format(
                getattr(obj, to_field, ''), escape(text), model_viewset.get_obj_url(self.request, obj)
            )

        return mark_safe(
            '<a href="{href}" {target} {data}>{text}</a>'.format(
                href=url,
                target='target="_blank"' if blank else '',
                data=data,
                text=text
            )
        )

    def handle_model(self, obj, field, value):
        return self.get_obj_link(value)

    def handle_qs(self, obj, field, value):
        return mark_safe(', '.join(self.get_obj_link(x) for x in value))

    def handle_bool(self, obj, field, value):
        if self.bool_as_icon:
            return mark_safe(
                '<i class="fas fa-{}-circle text-{}"></i>'.format(
                    value and 'check' or 'times', value and 'success' or 'danger'
                )
            )
        return super().handle_bool(obj, field, value)

    def handle_file(self, obj, field, value):
        if value:
            return mark_safe('<a href="{}" target="_blank">{}</a>'.format(value.url, value))
