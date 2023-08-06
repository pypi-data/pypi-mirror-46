from functools import partial, wraps

from django import forms


def formset_validate(func):
    @wraps(func)
    def wrapper(self, form):
        if forms.all_valid(self.formsets.values()):
            return func(self, form)
        return self.form_invalid(form)
    return wrapper


def check_permission_before(func):
    """Check permission before calling function"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        obj = getattr(self, 'object', None)
        if self.check_permission(self.request, obj):
            return func(self, *args, **kwargs)
        return self.permission_denied(obj)
    return wrapper


def check_permission_after(func):
    """Check permission before after function"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        obj = getattr(self, 'object', None)
        if not self.check_permission(self.request, obj):
            return self.permission_denied(obj)
        return result
    return wrapper


def add_form_formfield_callback(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        form = func(self, *args, **kwargs)
        return forms.modelform_factory(
            model=getattr(form.Meta, 'model', self.model),
            form=form,
            formfield_callback=partial(
                self.model_viewset.formfield_callback,
                request=self.request,
                lookups=self.model_viewset.lookups,
                autocomplete=self.model_viewset.autocomplete,
            )
        )
    return wrapper


def add_formset_formfield_callback(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        formsets = func(self, *args, **kwargs)
        for formset in formsets.values():
            formset.form = forms.modelform_factory(
                model=formset.form.Meta.model,
                form=formset.form,
                formfield_callback=partial(
                    self.model_viewset.formfield_callback,
                    request=self.request,
                    lookups=self.model_viewset.formset_lookups.get(
                        formset.prefix, ()
                    ),
                    autocomplete=self.model_viewset.formset_autocomplete.get(
                        formset.prefix, ()
                    ),
                )
            )
        return formsets
    return wrapper


def add_filterset_formfield_callback(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        filterset = func(self, *args, **kwargs)
        for name, field in filterset.form.fields.items():
            if name in self.model_viewset.filterset_autocomplete \
                    or name in self.model_viewset.filterset_lookups:
                field.widget = self.model_viewset.formfield_callback(
                    db_field=self.model._meta.get_field(name),
                    request=self.request,
                    autocomplete=self.model_viewset.filterset_autocomplete,
                    lookups=self.model_viewset.filterset_lookups,
                    can_add_related=False,
                ).widget
        return filterset
    return wrapper
