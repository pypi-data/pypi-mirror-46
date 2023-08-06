from django_filters.views import BaseFilterView

from django.contrib.admin.utils import NestedObjects
from django.contrib.admin.widgets import url_params_from_lookup_dict
from django.db import router
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
)

from viewsets.decorators import check_permission_before
from viewsets.filters import ViewSetFilterSet, viewset_filterset_factory
from viewsets.mixins import (
    FormsetViewMixin, PermissionMixin, SerializerMixin, SuccessMessageMixin
)


__all__ = [
    'BaseViewSetView', 'ViewSetListView',
    'ViewSetCreateView', 'ViewSetUpdateView', 'ViewSetDeleteView',
    'ViewSetDetailView', 'ViewSetIndexView'
]


class BaseViewSetView(PermissionMixin):
    viewset = None
    model_viewset = None
    model = None
    opts = None
    action = None
    is_popup = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.action in ('create', 'update', 'detail') and not getattr(self, 'form_class', None):
            self.fields = self.fields or [x.name for x in self.opts.get_fields() if x.editable and not x.auto_created]

    def dispatch(self, request, *args, **kwargs):
        self.is_popup = bool(self.request.GET.get('_popup') or self.request.POST.get('_popup'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'opts': self.opts,
            'viewset': self.viewset,
            'model_viewset': self.model_viewset,
            'is_popup': self.is_popup,
            'to_field': self.request.GET.get('_to_field', ''),
        })
        return context

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        if self.viewset and self.action:
            template_names = [
                '{}/{}/{}_{}.html'.format(
                    self.viewset.namespace, self.opts.app_label, self.opts.model_name, self.action
                ),
                '{}/{}_{}.html'.format(self.viewset.namespace, self.opts.app_label, self.action),
                '{}/{}.html'.format(self.viewset.namespace, self.action)
            ]
        else:
            template_names = super().get_template_names()
        return template_names + ['viewsets/{}.html'.format(self.action)]

    def get_success_url(self):
        if self.request.POST.get('_continue'):
            return self.model_viewset.reverse('update', self.object.pk)
        if self.request.POST.get('_addanother'):
            return self.model_viewset.reverse('create')
        return self.model_viewset.reverse('list')


class ViewSetListView(SerializerMixin, BaseViewSetView, BaseFilterView, ListView):
    fields = None
    fields_names = None

    filterset_fields = ()
    filterset_order_by = None
    autocomplete_filterset_fields = ()

    paginate_by = 10
    autocomplete_paginate_by = 10

    search_fields = ()
    search_kwargs = {}
    autocomplete_search_fields = ()
    autocomplete_search_kwargs = {}

    as_json = None

    def check_permission(self, request, obj=None):
        return self.model_viewset.has_list_permission(self.request)

    def dispatch(self, request, *args, **kwargs):
        self.as_json = (request.GET.get('as') == 'json')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_popup or self.as_json and self.request.GET:
            qs = self.filter_lookup(qs)
        return qs

    def filter_lookup(self, qs):
        lookups = []
        for fk_lookup in self.model._meta.related_fkey_lookups:
            if callable(fk_lookup):
                fk_lookup = fk_lookup()
            lookups.append(url_params_from_lookup_dict(fk_lookup))
        for key, value in self.request.GET.items():
            if {key: value} in lookups:
                qs = qs.complex_filter({key: value})
        return qs

    def get_paginate_by(self, queryset):
        if self.as_json:
            return self.autocomplete_paginate_by
        return super().get_paginate_by(queryset)

    def get_filterset_class(self):
        if self.filterset_class:
            return self.filterset_class
        fields_var = 'autocomplete_filterset_fields' if self.as_json else 'filterset_fields'
        filterset_fields = getattr(self, fields_var, ())
        return viewset_filterset_factory(model=self.model, fields=filterset_fields)

    def get_search_kwargs(self):
        kwargs = (self.autocomplete_search_kwargs if self.as_json else self.search_kwargs).copy()
        kwargs['fields'] = self.autocomplete_search_fields if self.as_json else self.search_fields
        return kwargs

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        if issubclass(filterset_class, ViewSetFilterSet):
            kwargs.update({
                'order_by': self.filterset_order_by if self.filterset_order_by is not None else self.fields,
                'search_kwargs': self.get_search_kwargs()
            })
        return kwargs

    def get_json_response(self, context):
        data = {
            "results": [{
                "id": obj.pk,
                "text": str(obj)
            } for obj in context.get('object_list', ())]
        }
        if context.get('page_obj'):
            data.update({
                'pagination': {
                    'more': context['page_obj'].has_next()
                }
            })
        return JsonResponse(data)

    def render_to_response(self, context, **response_kwargs):
        if self.as_json:
            return self.get_json_response(context)
        return super().render_to_response(context, **response_kwargs)


class ViewSetDetailView(SerializerMixin, BaseViewSetView, DetailView):
    fields = None
    fields_names = None

    def check_permission(self, request, obj=None):
        return self.model_viewset.has_detail_permission(request, obj)


class ViewSetCreateView(SuccessMessageMixin, FormsetViewMixin, BaseViewSetView, CreateView):
    success_message = _('Object was created.')

    def check_permission(self, request, obj=None):
        return self.model_viewset.has_create_permission(request)

    def form_valid(self, form):
        result = super().form_valid(form)
        if self.is_popup:
            return render(
                self.request,
                'viewsets/popup_response.html',
                context={
                    'object': self.object,
                    'obj_url': self.model_viewset.get_obj_url(self.request, self.object)
                },
            )
        else:
            self.add_message()
        return result


class ViewSetUpdateView(SuccessMessageMixin, FormsetViewMixin, BaseViewSetView, UpdateView):
    success_message = _('Object was updated.')

    def check_permission(self, request, obj=None):
        return self.model_viewset.has_update_permission(request, obj)

    def form_valid(self, form):
        result = super().form_valid(form)
        if not self.is_popup:
            self.add_message()
        return result


class ViewSetDeleteView(BaseViewSetView, SuccessMessageMixin, DeleteView):
    success_message = _('Object was deleted.')

    def check_permission(self, request, obj=None):
        return self.model_viewset.has_delete_permission(request, obj)

    def get_to_delete(self, objs):
        collector = NestedObjects(using=router.db_for_write(self.model))
        collector.collect(objs)
        perms_needed = set()

        def format_callback(obj):
            opts = obj._meta
            no_edit_link = '{}: {}'.format(capfirst(opts.verbose_name), force_text(obj))
            if not self.viewset:
                return no_edit_link

            viewset = self.viewset.get_registered(obj.__class__)

            if viewset:
                try:
                    url = viewset.reverse('update', pk=obj.pk)
                except NoReverseMatch:
                    return no_edit_link

                if not viewset.has_delete_permission(self.request, obj):
                    perms_needed.add(opts.verbose_name)
                return format_html('{}: <a href="{}">{}</a>', capfirst(opts.verbose_name), url, obj)
            else:
                return no_edit_link

        to_delete = collector.nested(format_callback)
        protected = [format_callback(obj) for obj in collector.protected]
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return to_delete, model_count, perms_needed, protected

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        to_delete, model_count, perms_needed, protected = self.get_to_delete([self.object])
        context.update({
            'to_delete': to_delete,
            'model_count': model_count,
            'perms_needed': perms_needed,
            'protected': protected,
            'object_name': force_text(self.opts.verbose_name)
        })
        return context

    @atomic
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        to_delete, model_count, perms_needed, protected = self.get_to_delete([self.object])
        if perms_needed or protected:
            return redirect('.')
        self.object.delete()
        self.add_message()
        return redirect(self.get_success_url())


class ViewSetIndexView(PermissionMixin, TemplateView):
    template_name = 'viewsets/index.html'
    viewset = None

    @check_permission_before
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def check_permission(self, request, obj=None):
        return request.user.is_authenticated
