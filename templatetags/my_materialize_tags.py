from django import template
import os
from django.urls import reverse

register = template.Library()





@register.inclusion_tag('id_tag.html')
def id(field):
    return {'field': field}


@register.inclusion_tag('input_tag.html')
def text(field, clss='', init=''):
    return { 'type': 'text',
             'field': field,
             'class': clss,
             'init': init,
             }


@register.inclusion_tag('input_tag.html')
def date(field, clss=''):
    return { 'type': 'date',
             'field': field,
             'class': 'jqdatepicker ' + clss,
             }

@register.inclusion_tag('input_tag.html')
def email(field, clss=''):
    return { 'type': 'email',
             'field': field,
             'class': clss
             }


@register.inclusion_tag('input_tag.html')
def password(field, clss=''):
    return { 'type': 'password',
             'field': field,
             'class': clss
             }


@register.inclusion_tag('input_tag.html')
def textarea(field, clss=''):
    return { 'type': 'textarea',
             'field': field,
             'class': clss
             }

@register.inclusion_tag('input_tag.html')
def checkbox(field, clss=''):
    return { 'type': 'checkbox',
             'field': field,
             'class': clss
             }


@register.inclusion_tag('input_tag.html')
def select(field, clss='', selected='', choices=None):
    if choices:
        field.field.choices = choices
    return { 'type': 'select',
             'field': field,
             'class': clss,
             'selected_value': selected,
             }


@register.inclusion_tag('input_tag.html')
def radio(field, clss='', selected=''):
    return { 'type': 'radio',
             'field': field,
             'class': clss,
             'selected_value': selected,
             }


@register.inclusion_tag('input_tag.html')
def file(field, clss=''):
    return { 'type': 'file',
             'field': field,
             'class': clss
             }


@register.filter
def filename(value):
    return os.path.basename(value.file.name) if value else 'файл не загружен'


@register.inclusion_tag('tooltip_tag.html')
def tooltip(text, position='bottom', delay=1000):
    return {'text': text,
            'delay': delay,
            'position': position
            }


@register.inclusion_tag('paginator_tag.html', takes_context=True)
def paginator(context, split_by=10, form_filter=None):
    page_range = context['paginator'].page_range
    page_number = context['page_obj'].number
    reminder = page_number
    if reminder > split_by:
        reminder = reminder % split_by
        if reminder == 0: reminder = split_by
    first_page_insplit = page_number - reminder + 1
    last_page = page_range[-1]
    last_page_insplit = first_page_insplit + split_by
    if last_page_insplit > last_page: last_page_insplit = last_page + 1

    return {'is_paginated': context['is_paginated'],
            'paginator': context['paginator'],
            'page_obj': context['page_obj'],
            'range_insplit': range(first_page_insplit, last_page_insplit),
            'get_filter': get_filter(context, '&', form_filter)
            }


@register.simple_tag(takes_context=True)
def get_filter(context, first_prefix='?', form_filter=None):
    req_str = ''
    if form_filter != None:
        requests = []
        for field in context[form_filter]:
            if field.name in context['request'].GET:
                requests.append(field.name + '=' + context['request'].GET[field.name])
        if requests:
            p = first_prefix
            for r in requests:
                req_str += (p + r)
                p = '&'
    return req_str


@register.simple_tag(takes_context=True)
def active(context, name):
    path = reverse(name)
    if context['request'].path == path:
        return 'active'
    return ''