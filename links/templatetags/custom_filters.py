
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def teachers(teachers):
    return mark_safe(''.join([
        f'<span>{teacher}</span>'
        for teacher in teachers.split(', ')
    ]))


@register.filter
def links(links):
    return mark_safe(''.join([
        f'<div><a href="{link}">{link}</a></div>'
        for link in links.split('\n')
    ]))
