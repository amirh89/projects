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


def add_something(request, object_form):
    if request.method == 'POST':
        form = object_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hobby:home')
    else:
        form = object_form()
    return render(request, 'forms/add_something.html', {'form':form})


@login_required
def add_category(request):
    return add_something(request, CategoryForm)


@login_required
def add_object(request):
    return add_something(request, ObjectForm)


def objects_of_category(request, name):
    category = get_object_or_404(Category, name=name)
    objs = category.objs.all()
    return render(request, 'reading/objects_of_category.html', {'category':category, 'objs':objs})


class ObjectList(ListView):
    model = Object
    template_name = 'reading/object_list.html'
    context_object_name = 'objects'
    paginate_by = 5


def object_detail(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    form = CommentForm()
    comments = obj.comments.all()[:3]
    return render(request, 'reading/object_detail.html', {'obj':obj,'form':form,'comments':comments})


def comments_of_objects(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    comments = obj.comments.all()
    return render(request, 'reading/comments_of_objects.html', {'obj':obj,'comments':comments})


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


def control_object_actions(request, action):
    object_id = request.POST.get('object_id')
    if object_id is None:
        return JsonResponse({'error':'invalid'})
    
    object = get_object_or_404(Object, id=object_id)
    user = request.user

    action_list = getattr(object, action)

    if user in action_list.all():
        action_list.remove(user)
        action_status = False
    else:
        action_list.add(user)
        action_status = True

    response = {
        action:action_status,
        f'{action}_count':action_list.count()
    }

    return JsonResponse(response)


@login_required
@require_POST
def like_object(request):
    return control_object_actions(request, 'like')


@login_required
@require_POST
def save_object(request):
    return control_object_actions(request, 'saved_by')
