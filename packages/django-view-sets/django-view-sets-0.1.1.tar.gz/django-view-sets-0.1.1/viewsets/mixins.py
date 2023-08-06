from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic

from viewsets.decorators import formset_validate
from viewsets.serializers import ViewSetSerializer


class SuccessMessageMixin:
    """
    Add a success message.
    """
    success_message = ''

    def get_success_message(self):
        return self.success_message

    def add_message(self):
        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)


class FormsetMeta(type):
    """Add decorator to form_valid for checking formsets"""

    def __init__(cls, name, bases, nmspc):
        super(FormsetMeta, cls).__init__(name, bases, nmspc)
        cls.form_valid = formset_validate(cls.form_valid)


class FormsetViewMixin(metaclass=FormsetMeta):
    formset_classes = ()
    sortable_field_names = {}
    default_sortable_field_name = 'position'
    formsets = None

    def get_formset_classes(self):
        return self.formset_classes

    def get_formsets(self):
        formsets = {}
        for formset_class in self.get_formset_classes():
            formset = formset_class(**self.get_formset_kwargs())
            formset.opts = formset.model._meta
            formsets[formset.prefix] = formset
        return formsets

    def get_form(self):
        self.formsets = self.get_formsets()
        return super().get_form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_and_formsets_media = context['form'].media
        for formset in self.formsets.values():
            form_and_formsets_media += formset.media
        context.update({
            'formsets': self.formsets,
            'form_and_formsets_media': form_and_formsets_media
        })
        return context

    def get_sortable_field(self, prefix):
        return self.sortable_field_names.get(
            prefix, self.default_sortable_field_name
        )

    def formsets_save(self):
        for formset in self.formsets.values():
            formset.instance = self.object
            if formset.can_order:
                sortable_field = self.get_sortable_field(formset.prefix)
                for i, formset_form in enumerate(formset.ordered_forms):
                    if getattr(formset_form.instance, sortable_field) != i:
                        formset_form.has_changed = lambda: True
                    setattr(formset_form.instance, sortable_field, i)
            formset.save()

    @atomic
    def form_valid(self, form):
        result = super().form_valid(form)
        self.formsets_save()
        return result

    def get_formset_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if getattr(self, 'object', None):
            kwargs['instance'] = self.object
        return kwargs


class PermissionMixin:
    def permission_denied(self, obj=None):
        raise PermissionDenied

    def check_permission(self, request, obj=None):
        raise NotImplementedError

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if hasattr(self, 'model_viewset'):
            for action in ('create', 'update', 'delete', 'list', 'detail'):
                perm_name = 'has_{}_permission'.format(action)
                perm = getattr(self.model_viewset, perm_name)
                perm_args = [self.request]
                if action not in ('create', 'list'):
                    perm_args.append(getattr(self, 'object', None))
                context[perm_name] = perm(*perm_args)
        return context


class SerializerMixin:
    serializer = ViewSetSerializer
    bool_as_icon = True
    default_value = ''

    def get_serializer_class(self):
        return self.serializer

    def get_serializer_kwargs(self, **kwargs):
        order_fields = ()
        if hasattr(self, 'filterset'):
            order_fields = getattr(self.filterset, 'order_fields', ())
        kwargs.update({
            'request': self.request,
            'model_viewset': self.model_viewset,
            'instance': getattr(self, 'object', None),
            'fields': getattr(self, 'fields', ()),
            'fields_names': getattr(self, 'fields_names', {}),
            'default_value': self.default_value,
            'order_fields': order_fields,
            'bool_as_icon': self.bool_as_icon,
        })
        return kwargs

    def get_serializer(self, **kwargs):
        serializer = self.get_serializer_class()
        if serializer:
            return serializer(**self.get_serializer_kwargs(**kwargs))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['serializer'] = self.get_serializer(
            object_list=context.get('object_list')
        )
        return context


class DjangoPermissionMixin:
    def has_list_permission(self, request):
        codename_view = get_permission_codename('view', self.opts)
        return request.user.has_perm('%s.%s' % (self.opts.app_label, codename_view))

    def has_create_permission(self, request):
        codename = get_permission_codename('add', self.opts)
        return request.user.has_perm('%s.%s' % (self.opts.app_label, codename))

    def has_update_permission(self, request, obj=None):
        codename = get_permission_codename('change', self.opts)
        return request.user.has_perm('%s.%s' % (self.opts.app_label, codename))

    def has_delete_permission(self, request, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return request.user.has_perm('%s.%s' % (self.opts.app_label, codename))

    def has_detail_permission(self, request, obj=None):
        codename_view = get_permission_codename('view', self.opts)
        codename_change = get_permission_codename('change', self.opts)
        return (
            request.user.has_perm('%s.%s' % (self.opts.app_label, codename_view)) or
            request.user.has_perm('%s.%s' % (self.opts.app_label, codename_change))
        )
