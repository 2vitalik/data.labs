import re

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


def make_link(href):
    if not href:
        return ''

    if not href.startswith('http'):
        return f'<i style="color: gray;">{href}</i>'

    prefix = ''
    title = href

    if m := re.fullmatch(r'https://dl\.nure\.ua/course/view\.php\?id=(\d+)', href):
        prefix = 'dl(course):'
        title = m.group(1)
    elif m := re.fullmatch(r'https://dl\.nure\.ua/mod/url/view\.php\?id=(\d+)', href):
        prefix = 'dl(url):'
        title = m.group(1)
    elif m := re.fullmatch(r'https://dl\.nure\.ua/mod/forum/view\.php\?id=(\d+)', href):
        prefix = 'dl(forum):'
        title = m.group(1)
    elif m := re.fullmatch(r'https://dl\.nure\.ua/mod/attendance/view\.php\?id=(\d+)', href):
        prefix = 'dl(attend):'
        title = m.group(1)
    elif m := re.fullmatch(r'https://classroom\.google\.com/(.*)', href):
        prefix = f'classroom:'
        title = m.group(1)
    elif m := re.fullmatch(r'https://t\.me/(.*)', href):
        prefix = f'telegram:'
        title = m.group(1)
    elif m := re.fullmatch(r'https://meet\.google\.com/(\w{3}-\w{4}-\w{3})', href):
        prefix = 'meet:'
        title = m.group(1)
    elif m := re.fullmatch(r'https://[\w-]+\.zoom\.us/j/(\d+).*', href):
        prefix = f'zoom:'
        title = m.group(1)

    return f'<div>{prefix} <a href="{href}">{title}</a></div>'


@register.filter
def links(links):
    return mark_safe(''.join([
        make_link(link.strip())
        for link in links.split('\n')
    ]))
