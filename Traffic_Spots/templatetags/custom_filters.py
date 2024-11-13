from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    return value.split(delimiter)

@register.filter
def trim(value):
    """Trims leading and trailing whitespace from the string."""
    return value.strip()