from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo
from .forms import TodoForm

# Create your views here.

def index(request):
    item_list = Todo.objects.order_by('-date')
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo')
    form = TodoForm()
    context = {
        'forms':form,
        'list':item_list,
        'title':'TODO LIST'
    }
    return render(request, 'todo/index.html', context)


def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, 'item removed!')
    return redirect('todo')


def edit(request, item_id):
    item = get_object_or_404(Todo, id=item_id)

    if request.method == 'GET':
        context = {
            'form':TodoForm(instance=item),
            'id':item_id,
        }
        return render(request, 'todo/edit.html', context)
    elif request.method == 'POST':
        form = TodoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('todo')
        else:
            form = TodoForm()
    return render(request, 'todo/edit.html', {'form':form})
