from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

# Create your views here.

def home(request):
    return render(request, 'learning/home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            customer = Customer.objects.create(
            username = cd['username'],
            email = cd['email'],
            password = cd['password'],)
            customer.save()
            return redirect('learning:user_login')
    else:
        form = RegisterForm()
    return render(request, 'forms/signup.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = UserLogin.objects.create(
            username = cd['username'],
            password = cd['password'])
            obj.save()
            return redirect('learning:welcome')
    else:
        form = LoginForm()
    return render(request, 'forms/user_login.html', {'form':form})


@login_required
def welcome(request):
    return render(request, 'learning/welcome.html')


def profile(request, pk):
    user = get_object_or_404(UserLogin, pk=pk)
    form = LoginForm()
    context = {
        'user':user,
        'form':form,
    }
    return render(request, 'learning/profile.html', context)


def logout(request, pk):
    user = UserLogin.objects.filter(pk=pk)
    user.delete()
    return redirect('learning:home')


import datetime
def package_detail(request, pk):
    package = get_object_or_404(LearningPackage, pk=pk)
    return render(request, 'learning/pack_detail.html', {"package":package, 'new_date':datetime.datetime.now})


def add_to_cart(request, pk):
    pack = get_object_or_404(LearningPackage, pk=pk)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = Cart.objects.create(
                package = pack,
                customer = cd['customer'],
                quantity = cd['quantity'],
                price = pack.price_with_discount*cd['quantity'],
                phone = cd['phone'],
            )
            obj.save()
            return redirect('learning:home')
    else:
        form = AddToCartForm()
    return render(request, 'forms/add_to_cart.html', {"form":form})


class CartList(ListView):
    queryset = Cart.objects.all()
    context_object_name = 'packs'
    paginate_by = 10
    template_name = 'learning/cart_list.html'
