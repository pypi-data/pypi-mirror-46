from django.db import models
from django.urls import NoReverseMatch, include, path, reverse, reverse_lazy

from viewsets.decorators import (
    add_filterset_formfield_callback, add_form_formfield_callback,
    add_formset_formfield_callback, check_permission_after,
    check_permission_before
)
from viewsets.views import (
    ViewSetCreateView, ViewSetDeleteView, ViewSetDetailView, ViewSetListView,
    ViewSetUpdateView
)
from viewsets.widgets import (
    AutocompleteManyWidget, AutocompleteWidget, LookupWidget,
    RelatedWidgetWrapper
)


class Default:
    pass


class ViewSet:
    """
    The Viewset class is a container for `ModelViewSet`s.
    """
    def __init__(self, namespace='', name='', view_index=None):
        self.namespace = namespace
        self.prefix = '{}:'.format(self.namespace) if self.namespace else ''
        self.name = name or self.namespace
        self.view_index = view_index
        self._registry = {}

    @property
    def urls(self):
        return self.get_urls(), self.namespace, self.name

    @property
    def registered(self):
        return self._registry.items()

    def get_registered(self, model):
        return self._registry.get(model)

    def register(self, model, model_viewset=None, model_namespace=None, **viewset_kwargs):
        """
        Register the given model with the given model_viewset class.
        """
        model_viewset = model_viewset or ModelViewSet
        self._registry[model] = model_viewset(
            model=model, viewset=self, model_namespace=model_namespace, **viewset_kwargs
        )

    def get_urls(self):
        """
        Get all registered urls.
        """
        urls = []
        if self.view_index:
            urls += [path('', self.view_index.as_view(viewset=self), name='index')]
        for model, viewset in self.registered:
            urls += [path('{}/'.format(viewset.model_namespace), include(viewset.urls))]
        return urls

    def get_index_url(self):
        return reverse_lazy('{}index'.format(self.prefix))

    def reverse(self, model, name, *args, **kwargs):
        """
        Get url for the given model.
        """
        try:
            model_viewset = self._registry[model]
            url = model_viewset.reverse(name, *args, **kwargs)
        except (KeyError, NoReverseMatch):
            url = ''
        return url

    def get_obj_url(self, request, obj):
        try:
            model_viewset = self._registry[obj.__class__]
            url = model_viewset.get_obj_url(request, obj)
        except (KeyError, NoReverseMatch):
            url = ''
        return url


class ViewAttrsMixin:
    fields = Default
    fields_names = Default
    serializer = Default
    queryset = Default
    form_class = Default
    formset_classes = Default

    filterset_fields = Default
    filterset_order_by = Default
    autocomplete_filterset_fields = Default

    paginate_by = Default
    autocomplete_paginate_by = Default

    search_fields = Default
    search_kwargs = Default
    autocomplete_search_fields = Default
    autocomplete_search_kwargs = Default

    bool_as_icon = Default
    default_value = Default
    extra_context = Default


class ModelViewSet(ViewAttrsMixin):
    """
    The ModelViewSet class provides CRUD for model.
    """
    view_list = ViewSetListView
    view_create = ViewSetCreateView
    view_update = ViewSetUpdateView
    view_detail = ViewSetDetailView
    view_delete = ViewSetDeleteView

    base_mixin = None
    available_views = None

    lookups = ()
    autocomplete = ()
    formset_lookups = {}
    formset_autocomplete = {}
    filterset_lookups = ()
    filterset_autocomplete = ()

    def __init__(self, model, viewset=None, model_namespace=None, **kwargs):
        self.model = model
        self.viewset = viewset
        self.viewset_prefix = viewset and viewset.prefix or ''
        self.opts = model._meta
        self.model_namespace = model_namespace or self.opts.model_name
        self.available_views = self.available_views or ['list', 'create', 'update', 'detail', 'delete']

        for k, v in kwargs.items():
            setattr(self, k, v)

    def construct_view(self, view):
        """
        Create mixin from base_mixin and add decorators.
        """
        bases = (view,)
        if self.base_mixin:
            bases = (self.base_mixin,) + bases
        mixined_view = type('{}Mixined'.format(view.__name__), bases, {})
        mixined_view = self.add_decorators(mixined_view)
        return mixined_view

    def add_decorators(self, view):
        if hasattr(view, 'check_permission'):
            view.dispatch = check_permission_before(view.dispatch)
            if hasattr(view, 'get_object'):
                view.get_object = check_permission_after(view.get_object)
        if hasattr(view, 'get_form_class'):
            view.get_form_class = add_form_formfield_callback(view.get_form_class)
        if hasattr(view, 'get_formsets'):
            view.get_formsets = add_formset_formfield_callback(view.get_formsets)
        if hasattr(view, 'get_filterset'):
            view.get_filterset = add_filterset_formfield_callback(view.get_filterset)
        return view

    def get_view(self, view, action='', **view_kwargs):
        view = self.construct_view(view)
        return view.as_view(**self.get_view_kwargs(view, action, **view_kwargs))

    def get_view_kwargs(self, view, action, **view_kwargs):
        kwargs = {
            'viewset': self.viewset,
            'model_viewset': self,
            'opts': self.opts,
            'action': action,
        }
        for attr in (x for x in dir(ViewAttrsMixin) if not x.startswith('_')):
            kwargs.setdefault(attr, getattr(self, attr))
            if attr in ['fields', 'fields_names', 'serializer', 'queryset', 'form_class', 'formset_classes']:
                prefixed = '{}_{}'.format(action, attr)
                if hasattr(self, prefixed):
                    kwargs[attr] = getattr(self, prefixed)
        kwargs.update(view_kwargs)
        return {k: v for k, v in kwargs.items() if hasattr(view, k) and v is not Default}

    def reverse(self, view_name, *args, **kwargs):
        try:
            return reverse(
                '{}{}:{}'.format(self.viewset_prefix, self.model_namespace, view_name),
                args=args,
                kwargs=kwargs
            )
        except NoReverseMatch:
            return ''

    @classmethod
    def as_crud(cls, **kwargs):
        """
        Initialize ModelViewset instance and return included urlpatterns.
        """
        return include(cls(**kwargs).urls)

    def get_urls(self):
        urls = []
        patterns = (
            ('list', ''),
            ('create', 'add/'),
            ('detail', '<slug:pk>/'),
            ('update', '<slug:pk>/change/'),
            ('delete', '<slug:pk>/delete/')
        )
        for view_name, pattern in patterns:
            if view_name in self.available_views:
                view = getattr(self, 'view_{}'.format(view_name))
                urls.append(path(pattern, self.get_view(view, view_name, model=self.model), name=view_name))
        return urls

    @property
    def urls(self):
        return self.get_urls(), self.model_namespace

    def has_list_permission(self, request):
        return 'list' in self.available_views and request.user.is_authenticated

    def has_create_permission(self, request):
        return 'create' in self.available_views and request.user.is_authenticated

    def has_update_permission(self, request, obj=None):
        return 'update' in self.available_views and request.user.is_authenticated

    def has_delete_permission(self, request, obj=None):
        return 'delete' in self.available_views and request.user.is_authenticated

    def has_detail_permission(self, request, obj=None):
        return 'detail' in self.available_views and request.user.is_authenticated

    def get_obj_url(self, request, obj):
        if self.has_detail_permission(request, obj):
            return self.reverse('detail', pk=obj.pk)
        if self.has_update_permission(request, obj):
            return self.reverse('update', pk=obj.pk)
        return ''

    def formfield_callback(self, db_field, request, lookups=(), autocomplete=(), can_add_related=True, **kwargs):
        if self.viewset and isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            url = self.viewset.reverse(db_field.remote_field.model, 'list')
            if isinstance(db_field, models.ManyToManyField) and db_field.name in autocomplete and url:
                kwargs['widget'] = AutocompleteManyWidget(
                    rel=db_field.remote_field,
                    url=url
                )
            elif isinstance(db_field, models.ForeignKey) and db_field.name in lookups and url:
                kwargs['widget'] = LookupWidget(
                    rel=db_field.remote_field,
                    list_url=url,
                    obj_url_fn=lambda obj: self.viewset.get_obj_url(request, obj),
                    using=kwargs.get('using')
                )
            elif db_field.name in autocomplete and url:
                kwargs['widget'] = AutocompleteWidget(rel=db_field.remote_field, url=url)

            if 'widget' in kwargs and can_add_related:
                related_viewset = self.viewset.get_registered(db_field.remote_field.model)
                if related_viewset and related_viewset.has_create_permission(request):
                    kwargs['widget'] = RelatedWidgetWrapper(
                        widget=kwargs['widget'],
                        add_related_url=self.viewset.reverse(db_field.remote_field.model, 'create'),
                        can_add_related=can_add_related,
                    )
        return db_field.formfield(**kwargs)
