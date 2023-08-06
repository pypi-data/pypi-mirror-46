from django.template import library
from django.template.defaultfilters import unordered_list
from django.utils.http import urlencode


try:
    from django_jinja import library as jinja_library
    import jinja2
except ImportError:
    jinja_library = None

register = library.Library()


@register.simple_tag()
def viewset_url(model_viewset, view_name, *args, **kwargs):
    return model_viewset.reverse(view_name, *args, **kwargs)


@register.simple_tag()
def object_url(viewset, obj, view_name='detail', *args, **kwargs):
    model_viewset = viewset.get_registered(obj.__class__)
    return viewset_url(model_viewset, view_name, *args, **kwargs)


@register.simple_tag(takes_context=True)
def has_perm(context, viewset, perm, *args, **kwargs):
    perm_fn = getattr(viewset, 'has_{}_permission'.format(perm))
    return perm_fn(context['request'], *args, **kwargs)


@register.inclusion_tag('viewsets/includes/_sort_link.html', takes_context=True)
def sort_link(context, field_name, title, sorting):
    if not sorting:
        return {'sorting': False, 'title': title}
    request = context['request']
    filterset = context['filter']
    param = filterset.order_fields.get(field_name)
    order = request.GET.get('o', '')
    order_by = order.lstrip('-')
    direction = ''
    is_ordered = False
    if param == order_by:
        is_ordered = True
        if order == order_by:
            direction = '-'
    return {
        'name': field_name,
        'title': title,
        'sorting': sorting,
        'direction': direction,
        'is_ordered': is_ordered,
        'param': param
    }


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter()
def order_formset_forms(formset):
    # Sort in right order if formset has errors
    if formset.can_order and formset.is_bound:
        return sorted(formset, key=lambda x: x.cleaned_data.get('ORDER', None))
    return formset


@register.inclusion_tag('viewsets/includes/_paginator.html', takes_context=True)
def show_paginator(context):
    page_obj = context['page_obj']
    number = page_obj.number
    num_pages = page_obj.paginator.num_pages
    before = [x for x in range(number - 2, number) if x > 0]
    after = [x for x in range(number + 1, number + 3) if x <= num_pages]
    context.update({
        'range_pages': before + [number] + after
    })
    return context


@register.simple_tag(takes_context=True)
def preserve_params(context, encoded=False):
    request = context['request']
    params = request.GET.dict().copy()
    filterset = context.get('filter')
    if filterset:
        params = {k: v for k, v in params.items() if k not in filterset.filters}
    if encoded:
        return urlencode(params)
    return params


@register.filter()
def is_widget_type_of(field, widget_type):
    return hasattr(field.field.widget, 'input_type') and field.field.widget.input_type == widget_type


@register.filter()
def add_css_class(field, css_class):
    classes = field.field.widget.attrs.get('class', '')
    field.field.widget.attrs['class'] = ' '.join([classes, css_class]).strip()
    return field


@register.filter()
def add_error_css_class(field, css_class):
    if field.errors:
        add_css_class(field, css_class)
    return field


if jinja_library:
    @jinja_library.global_function(name='show_paginator')
    @jinja_library.render_with('viewsets/includes/_paginator.html')
    @jinja2.contextfunction
    def _show_paginator(context):
        return show_paginator(dict(context))

    @jinja_library.global_function(name='sort_link')
    @jinja_library.render_with('viewsets/includes/_sort_link.html')
    @jinja2.contextfunction
    def _sort_link(context, field_name, title, sorting):
        return sort_link(dict(context), field_name, title, sorting)

    jinja_library.global_function(viewset_url)
    jinja_library.global_function(object_url)
    jinja_library.global_function(jinja2.contextfunction(url_replace))
    jinja_library.global_function(jinja2.contextfunction(preserve_params))
    jinja_library.filter(order_formset_forms)
    jinja_library.filter(unordered_list)
    jinja_library.filter(fn=add_css_class, name='add_css_class')
    jinja_library.filter(fn=is_widget_type_of, name='is_widget_type_of')
    jinja_library.filter(fn=add_error_css_class, name='add_error_css_class')
