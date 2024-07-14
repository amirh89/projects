from django import template
from ..models import  *
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(name='catg')
def categories():
    return Category.objects.count()

@register.simple_tag
def products_of_categories():
    return Category.objects.annotate(products_count=Count('products'))

@register.simple_tag()
def most_popular_category(count:5):
    return Category.objects.annotate(products_count=Count('products')).order_by('-products_count')[:count]

@register.simple_tag
def customer_detail():
    return Customer.objects.all()

@register.simple_tag
def the_most_allowance(count:5):
    return Product.objects.annotate(allowance_amount_count=Count('allowance_amount')).order_by('-allowance_amount')[:count]

@register.simple_tag()
def the_most_popular_product(count:5):
    return Product.objects.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]

@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
