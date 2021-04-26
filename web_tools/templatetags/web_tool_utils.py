from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def add_span_tag(value):
    value = value.replace(" '", " <span style='font-weight: bold;'>'")
    return mark_safe(value.replace("' ", "'</span> "))
