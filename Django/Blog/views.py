from django.shortcuts import *
from django.http import *
from .models import *
from .forms import *
from django.core.paginator import *
from django.views.generic import *
from django.views.decorators.http import *
from django.views.decorators.csrf import *
from django.template import loader
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


@require_POST
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    like = None
    form = LikeForm(data=request.POST)
    if form.is_valid():
        like = form.save(commit=False)
        like.post = post
        like.save()
    context = {
        'post':post,
        'form':form,
        'like':like,
    }
    return render(request, 'forms/like.html', context)


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
            return HttpResponse("hi!. You loged in")
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form':form})


def logout_form(request, id):
    logout = Login.objects.filter(id=id)
    logout.delete()
    return render(request, 'forms/logout.html')


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


def profile(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.method == 'POST':
        form = ProfileForm2(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            pro_obj = Profile.objects.create(
                full_name = cd['full_name'],
                phone_number = cd['phone_number'],
                age = cd['age'],
                bio = cd['bio'],
            )
            pro_obj.save()
            return redirect(profile.get_absolute_url_3())
    else:
        form = ProfileForm2()
    return render(request, 'forms/prof.html', {'form':form})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    form = ProfileForm2()
    context = {
        'profile':profile,
        'form':form,
    }
    return render(request, 'forms/profile_detail.html', context)


def delete_profile(request, pk):
    profile = Profile.objects.filter(id=pk)
    profile.delete()
    return redirect('blog:index')


def edit_profile(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'GET':
        context = {
            'form':ProfileForm(instance=profile),
            'id':id,
        }
        return render(request, 'forms/edit_profile.html', context)
    
    elif request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(profile.get_absolute_url_3())
        else:
           form = ProfileForm()

    return render(request, 'forms/edit_profile.html', {'form':form})


def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    return redirect('blog:index')


def delete_comment(request, id):
    comment = Comment.objects.filter(post=id)
    comment.delete()
    return redirect('blog:post_list')


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': id}
        return render(request, 'forms/edit_post.html', context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponse(request, "The post updated ")
        else:
            return HttpResponse(request, "The post couldn't update ")
        
    return render(request,'forms/edit_post.html',{'form':form})


def edit_comment(request, id, comment_id):
    comment = get_object_or_404(Comment, post=id, id=comment_id)
    post = Post.objects.get(id=id)

    if request.method == 'GET':
        context = {'form': CommentForm(instance=comment), 'comment_id':id}
        return render(request, 'forms/edit_comment.html', context)
    
    elif request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
        
    return render(request, 'forms/edit_comment.html', {'form':form})


def fl_testing(request):
    data = Post.objects.filter(author__in=['1','2']).values()
    template = loader.get_template('forms/fl.html')
    context = {
        'data': data,
    }
    return HttpResponse(template.render(context, request))
