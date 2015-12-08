from django import template
from django import forms
register = template.Library()

@register.filter(name='values_list')
def values_list(queryset, attr):
    return queryset.values_list(attr, flat=True)


@register.filter(name='intersection')
def intersection(a, queryset):
    return bool(set(a) & set(queryset.values_list('pk', flat=True)))
