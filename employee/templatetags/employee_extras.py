
from django import template
register = template.Library()

@register.filter
def filter_sensitive_history(history_text, hidden_fields):
    """
    hidden_fields: list of field names and/or display labels
    Hide lines containing any of these (case-insensitive)
    """
    if not history_text:
        return []
    lines = history_text.split('\n')
    filtered = []
    # Lowercase all hidden fields for robust matching
    hidden_fields_lower = [str(f).lower() for f in hidden_fields]
    for line in lines:
        hide = False
        line_lower = line.lower()
        for field in hidden_fields_lower:
            if field in line_lower:
                hide = True
                break
        if not hide:
            filtered.append(line)
    return filtered

@register.filter
def get_field_display(obj, field_name):
    value = getattr(obj, field_name, '')
    get_display = getattr(obj, f'get_{field_name}_display', None)
    if callable(get_display):
        return get_display()
    return value
