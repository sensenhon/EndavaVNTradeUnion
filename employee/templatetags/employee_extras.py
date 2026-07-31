import calendar
import re
from django import template
register = template.Library()

DATE_STR_RE = re.compile(r"'(\d{4})-(\d{2})-(\d{2})'")

def redact_dob_year(line):
    def repl(match):
        month = int(match.group(2))
        day = int(match.group(3))
        month_name = calendar.month_name[month]
        return f"{month_name} {day}"
    return DATE_STR_RE.sub(repl, line)

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
    hidden_fields_lower = [str(f).lower() for f in hidden_fields]
    for line in lines:
        line_lower = line.lower()
        if 'date of birth' in line_lower:
            line = redact_dob_year(line)
            line_lower = line.lower()
        hide = False
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

@register.filter
def dict_get(d, key):
    if not isinstance(d, dict):
        return ''
    return d.get(key, '')