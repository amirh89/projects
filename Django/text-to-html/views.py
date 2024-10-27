from django.shortcuts import render
from .forms import *

# Create your views here.

def convert_text_to_html(request):
    form = TextConvertorForm()
    return render(request, 'forms/index.html', {'form':form})
