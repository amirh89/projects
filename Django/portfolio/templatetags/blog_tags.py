from django import template
from markdown import markdown
from django.utils.safestring import mark_safe
from ..models import *
from django.db.models import Count

register = template.Library()

@register.simple_tag
def objects_of_categories():
    return Category.objects.annotate(objs_count=Count('objs'))


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
