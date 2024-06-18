from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.views.generic import ListView
import datetime
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'store/home.html')


def login(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            customer = Customer.objects.create(
                first_name = cd['first_name'],
                last_name = cd['last_name'],
                phone = cd['phone'],
                email = cd['email'],
                password = cd['password'],)
            customer.save()
            return redirect('store:home')
    else:
        form = CustomerForm()
    return render(request, 'forms/login.html', {'form':form})


def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            product_object = Product.objects.create(
                name = cd['name'],
                price = cd['price'],
                category = cd['category'],
                description = cd['description'],
                image = cd['image'],)
            product_object.save()
            return redirect('store:home')
    else:
        form = ProductForm()
    return render(request, 'forms/product.html', {'form':form})


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 5
    template_name = 'store/product_list.html'


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    comments = product.comments.filter(active=True)
    form = CommentForm()
    allowance = product.allowances.all()
    context = {
        'product': product,
        'new_date': datetime.datetime.now(),
        'form': form,
        'comments': comments,
        'allowance': allowance,
    }
    return render(request, 'store/product_detail.html', context)


@require_POST
def product_comment(request, pk):
    product = get_object_or_404(Product, id=pk)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
    context = {
        'product':product,
        'comment':comment,
        'form':form,
    }
    return render(request, 'forms/comment.html', context)


def products_of_categories(request, id):
    category = get_object_or_404(Category, id=id)
    products = category.products.all()
    context = {
        'category':category,
        'products':products,
    }
    return render(request, 'forms/pfc.html', context)


class CartListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'carts'
    paginate_by = 5
    template_name = 'store/cart.html'


def add_to_cart(request, pk):
    product_id = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart = Order.objects.create(
                product = product_id,
                customer = cd['customer'],
                quantity = cd['quantity'],
                price = product_id.price*cd['quantity'],
                address = cd['address'],
                phone = cd['phone'],)
            cart.save()
            return redirect('store:home')
    else:
        form = OrderForm()
    return render(request, 'forms/add_to_cart.html', {'form': form})


def remove_from_cart(request, id):
    product = Order.objects.filter(id=id)
    product.delete()
    return redirect('store:cart')


def delete_all_products_from_cart(request):
    products = Order.objects.all()
    products.delete()
    return redirect('store:cart')


def allowance(request, pk):
    product_id = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = AllowanceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            allowance_obj = Allowance.objects.create(
                product = product_id,
                amount = cd['amount'],
                description = cd['description'],
            )
            allowance_obj.save()
            return redirect('store:home')
    else:
        form = AllowanceForm()
    return render(request, 'forms/allowance.html', {'form':form})


def delete_allowance(request, id):
    allowance = Allowance.objects.filter(product=id)
    allowance.delete()
    return redirect('store:home')


def search_bar(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(name__icontains=query)
        else:
            results = Product.objects.none()
        return render(request, 'forms/search.html', {'form':form, 'results':results})
