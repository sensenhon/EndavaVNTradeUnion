from django import template
register = template.Library()

@register.filter
def get_field_display(obj, field_name):
    value = getattr(obj, field_name, '')
    get_display = getattr(obj, f'get_{field_name}_display', None)
    if callable(get_display):
        return get_display()
    return value
