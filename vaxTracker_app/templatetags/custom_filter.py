from django import template

register = template.Library()

@register.filter
def custom_range(value):
    try:
        return range(value)
    except TypeError:
        return []
