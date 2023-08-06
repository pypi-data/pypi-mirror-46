import operator

import django_filters

from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class SearchFilter(django_filters.CharFilter):
    operator_choices = {
        'or': operator.or_,
        'and': operator.and_,
    }

    def __init__(self, *args, **kwargs):
        self.search_fields = kwargs.pop('fields', ())
        self.operator = kwargs.pop('operator', 'or')
        self.term_limit = kwargs.pop('term_limit', None)
        kwargs.setdefault('lookup_expr', 'icontains')
        placeholder = kwargs.pop('placeholder', _('Search'))
        super().__init__(*args, **kwargs)
        self.field.widget.attrs['placeholder'] = placeholder

    def get_operator(self):
        return self.operator_choices.get(self.operator)

    def filter(self, qs, value):
        if not value:
            return qs
        query = Q()
        query_operator = self.get_operator()
        terms = value.split()
        if self.term_limit:
            terms = terms[:self.term_limit]
        for term in terms:
            term_q = Q()
            for field_name in self.search_fields:
                term_q |= Q(**{
                    '{}__{}'.format(field_name, self.lookup_expr): term}
                )
            query = query_operator(query, term_q)
        qs = qs.filter(query)
        if self.distinct:
            qs = qs.distinct()
        return qs


class ViewSetFilterSet(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None,
                 search_kwargs=None, order_by=None):
        self.base_filters['o'] = django_filters.OrderingFilter(widget=forms.HiddenInput)
        sp = search_kwargs.pop('parameter', 'q')
        has_search = search_kwargs and search_kwargs.get('fields')
        if has_search:
            self.base_filters[sp] = SearchFilter(**search_kwargs)
        super().__init__(data, queryset, request=request, prefix=prefix)

        self.order_fields = {}
        if order_by:
            self.get_order_by(order_by)

        self.has_filters = bool(set(self.filters.keys()) - {'o', sp})
        self.search_field = self.form[sp] if has_search else None
        self.filter_fields = [x for x in self.form if x.name not in ('o', sp)]

    def get_order_by(self, order_by):
        model_fields_names = [
            x.name for x in self._meta.model._meta.get_fields()
        ]
        order_by = [
            x for x in order_by
            if x in model_fields_names or isinstance(x, (list, tuple))
        ]
        self.order_fields = self.filters['o'].normalize_fields(order_by)
        self.filters['o'].extra['choices'] = self.filters['o'].build_choices(
            self.order_fields, {}
        )


def viewset_filterset_factory(model, fields=forms.ALL_FIELDS):
    meta = type(
        'Meta', (object,),
        {
            'model': model,
            'fields': fields,
            'filter_overrides': {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                    },
                },
            }
        }
    )
    return type(
        '{}FilterSet'.format(model._meta.object_name),
        (ViewSetFilterSet,),
        {'Meta': meta}
    )
