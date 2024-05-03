from django import template
from ..models import  *
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()

# Post******************************
@register.simple_tag(name='tp')
def total_posts():
    return Post.published.count()

@register.simple_tag()
def last_post_date():
    return Post.published.last().publish

@register.simple_tag
def most_popular_posts(count:5):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]

@register.simple_tag
def most_popular_author():
    return Post.published.annotate(author_count=Count('author')).order_by('-author_count')

@register.simple_tag(name='rp')
def rej_posts():
    return Post.objects.filter(status='RJ').count()

@register.inclusion_tag('partials/latest_posts.html')
def latest_post(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context
# Post******************************

# Login******************************
@register.simple_tag(name='tl')
def total_login():
    return Login.objects.filter(active=True).count()

@register.simple_tag(name='nl')
def not_login():
    return Login.objects.filter(active=False).count()

@register.simple_tag(name='lld')
def last_login_date():
    return Login.objects.filter(active=False).last()

@register.simple_tag
def login():
    return Login.objects.filter(active=True).annotate(username_count=Count('username'))
# Login*******************************

# Comment*******************************
@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def total_profile():
    return Profile.objects.filter(active=True).count()
# Comment*******************************

# Ticket***********************************
@register.simple_tag()
def total_ticket_enteqad():
    return Ticket.objects.filter(subject='انتقاد').count()

@register.simple_tag(name='ttg')
def total_ticket_gozaresh():
    return Ticket.objects.filter(subject='گزارش').count()

@register.simple_tag(name='ttp')
def total_ticket_pishnahad():
    return Ticket.objects.filter(subject='پیشنهاد').count()
# Ticket*************************************

@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))

@register.simple_tag
def total_profile():
    return Profile.objects.filter(active=True).annotate(full_name_count=Count('full_name'))
