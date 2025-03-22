from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import *
from .models import *
from django.views.generic import ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'reading/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password_2'])
            user.save()
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form':form})


def log_out(request):
    logout(request)
    return HttpResponse('You have just logged out.')


def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('hobby:home')
    form = UserEditForm(instance=request.user)
    return render(request, 'forms/edit_user_form.html', {'form':form})


@login_required
def profile(request):
    user = request.user
    saved_objects = user.saved_objects.all()
    return render(request, 'reading/profile.html', {'user':user, 'saved_objects':saved_objects})


@login_required
@require_POST
def post_comment(request, pk):
    model = get_object_or_404(Object, id=pk)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.object = model
        comment.name = request.user.first_name
        comment.save()
    context = {
        'model':model,
        'form':form,
        'comment':comment,
    }
    return render(request, 'forms/post_comment.html', context)


def objects_of_category(request, name):
    category = get_object_or_404(Category, name=name)
    objs = category.objs.all()
    return render(request, 'reading/objects_of_category.html', {'category':category, 'objs':objs})


@login_required
def add_object(request):
    if request.method == 'POST':
        form = ObjectForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hobby:home')
    else:
        form = ObjectForm()
    return render(request, 'forms/add_object.html', {'form':form})


class ObjectList(ListView):
    model = Object
    template_name = 'reading/object_list.html'
    context_object_name = 'objects'
    paginate_by = 5


def object_detail(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    form = CommentForm()
    comments = obj.comments.all()
    return render(request, 'reading/object_detail.html', {'obj':obj,'form':form,'comments':comments})


@login_required
def edit_object(request, pk):
    obj = get_object_or_404(Object, id=pk)

    if request.method == 'GET':
        context = {
            'form':ObjectForm(instance=obj),
            'id':pk
        }
        return render(request, 'forms/edit_object.html', context)
    
    if request.method == 'POST':
        form = ObjectForm(request.POST, instance=obj, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(obj.get_absolute_url())

    else:
        form = ObjectForm()
    return render(request, 'forms/edit_object.html', {'form':form})


def search_object(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Object.objects.filter(title__icontains=query)
    else:
        results = Object.objects.none()
    context = {
        'form':form,
        'results':results,
    }
    return render(request, 'forms/search_object.html', context)


@login_required
@require_POST
def like_object(request):
    object_id = request.POST.get('object_id')
    if object_id is not None:
        object = get_object_or_404(Object, id=object_id)
        user = request.user

        if user in object.like.all():
            object.like.remove(user)
            liked = False
        else:
            object.like.add(user)
            liked = True

        likes_count = object.like.count()
        response = {
            'liked':liked,
            'likes_count':likes_count,
        }
    else:
        response = {'error':'invalid'}
    return JsonResponse(response)


@login_required
@require_POST
def save_object(request):
    object_id = request.POST.get('object_id')
    if object_id is not None:
        object = get_object_or_404(Object, id=object_id)
        user = request.user

        if user in object.saved_by.all():
            object.saved_by.remove(user)
            saved = False
        else:
            object.saved_by.add(user)
            saved = True

        saves_count = object.saved_by.count()
        response = {
            'saves_count':saves_count,
            'saved':saved
        }
    else:
        response = {'error':'invalid'}
    return JsonResponse(response)
