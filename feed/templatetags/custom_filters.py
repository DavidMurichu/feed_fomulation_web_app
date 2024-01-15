from django import template

register = template.Library()

@register.filter
def unique(values):
    return list(set(values))
