from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from translate import Translator

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/list.html'


import datetime
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post' : post,
        'new_date' : datetime.datetime.now(),
        'form' : form,
        'comments' : comments,
    }
    return render(request, "blog/detail.html", context)



def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_object = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_object.message = cd['message']
            ticket_object.name = cd['name']
            ticket_object.email = cd['email']
            ticket_object.phone = cd['phone']
            ticket_object.subject = cd['subject']
            ticket_object.save()
            return redirect('blog:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form':form})

def post_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Post.objects.create(
                author=request.user,
                title=cd['title'],
                description=cd['description'],
                reading_time=cd['reading_time'],
                vahed=cd['vahed'])
            ticket_obj.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'forms/postform.html', {'form':form})
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post' : post,
        'form' : form,
        'comment' : comment,
    }
    return render(request, 'forms/comment.html', context)

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            login_obj = Login.objects.create(
                password=cd['password'],
                username = cd['username'],
            )
            login_obj.save()
            return redirect('blog:index')
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form':form})

def counter(request):
    if request.method == 'POST':
        text = request.POST['texttocount']
        if text != '':
            word = len(text.split())
            i = True
            return render(request, 'forms/counter.html',
                          {'word': word, 'text' : text, 'i' : i, 'on':'active'})
        else:
            return render(request, 'forms/counter.html', {'on':'active'})
    else:
        return render(request, 'forms/counter.html', {'on':'active'})
    
def translate(request):
    if request.method == 'POST':
        text = request.POST['translate']
        language = request.POST['language']
        translator = Translator(to_lang=language)
        translation = translator.translate(text)
        return HttpResponse(translation)
    return render(request, 'forms/translate.html')

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            pro_obj = Profile.objects.create(
                full_name = cd['full_name'],
                phone_number = cd['phone_number'],
                age = cd['age'],
                bio = cd['bio'],
            )
            pro_obj.save()
            return redirect('blog:index')
    else:
        form = ProfileForm()
    return render(request, 'forms/prof.html', {'form':form})
