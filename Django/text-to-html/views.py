from django.shortcuts import render, HttpResponse
from .forms import *

# Create your views here.

def home(request):
    form = MyForm()
    return render(request, 'forms/index.html', {'form':form})
