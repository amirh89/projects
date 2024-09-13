from django.shortcuts import *
from django.http import JsonResponse
from .models import *
from .forms import *
from .serializer import *
from django.views.generic import ListView
import datetime
from django.views.decorators.http import require_POST
from rest_framework import generics
from django.contrib.auth import login as lg, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


def logout(request, pk):
    customer = Customer.objects.filter(id=pk)
    customer.delete()
    return redirect('store:home')


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    form = CustomerForm()
    context = {
        'customer':customer,
        'form':form,
    }
    return render(request, 'store/customer_detail.html', context)


def edit_profile(request, pk):
    profile = get_object_or_404(Customer, id=pk)

    if request.method == 'GET':
        context = {'form':CustomerModelForm(instance=profile), 'id':pk}
        return render(request, 'forms/edit_profile.html', context)
    
    if request.method == 'POST':
        customer_form = CustomerModelForm(request.POST, instance=profile)
        if customer_form.is_valid():
            customer_form.save()
            return redirect(profile.get_absolute_url())
    else:
        form = CustomerModelForm()

    return render(request, 'forms/edit_profile.html', {'form':form})


def product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            cd = product_form.cleaned_data
            product_object = Product.objects.create(
                name = cd['name'],
                price = cd['price'],
                category = cd['category'],
                description = cd['description'],
                image = cd['image'],
                allowance_amount = cd['allowance_amount'],
                text = cd['text'],)
            product_object.save()
            return redirect('store:home')
    else:
        form = ProductForm()
    return render(request, 'forms/add_product.html', {'form':form})


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 5
    template_name = 'store/product_list.html'


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    comments = product.comments.filter(active=True)
    form = CommentForm()
    price = (product.allowance_amount/100)*product.price
    new_price = product.price - price
    context = {
        'product': product,
        'new_date': datetime.datetime.now(),
        'form': form,
        'comments': comments,
        'new_price': new_price,
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


def delete_comment(request, id, pk):
    comment = Comment.objects.filter(product_id=pk, id=id)
    comment.delete()
    return redirect('store:home')


def products_of_categories(request, id):
    category = get_object_or_404(Category, id=id)
    products = category.products.all()
    context = {
        'category':category,
        'products':products,
    }
    return render(request, 'store/pfc.html', context)


def add_to_cart(request, pk):
    product_id = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            cd = order_form.cleaned_data
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


class CartListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'carts'
    paginate_by = 5
    template_name = 'store/cart.html'


def remove_from_cart(request, id):
    product = Order.objects.filter(id=id)
    product.delete()
    return redirect('store:cart')


def delete_all_products_from_cart(request):
    products = Order.objects.all()
    products.delete()
    return redirect('store:cart')


def add_to_favorite(request, pk):
    product_id = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        favorite_form = FavoriteForm(request.GET)
        if favorite_form.is_valid():
            favorite = Favorite.objects.create(
                product = product_id,
            )
            favorite.save()
            return redirect('store:favorite_list')
    else:
        form = FavoriteForm()
    return render(request, 'forms/add_to_favorite.html', {'form':form})


class FavoritesList(ListView):
    queryset = Favorite.objects.all()
    context_object_name = 'favorites'
    paginate_by = 3
    template_name = 'store/favorite_list.html'


def remove_product_from_favorite_list(request, id):
    product = Favorite.objects.filter(id=id)
    product.delete()
    return redirect('store:favorite_list')


def search_bar(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.all()
    context = {
        'form':form,
        'results':results,
    }
    return render(request, 'forms/search.html', context)
    

def compare_products(request):
    if request.method == 'POST':
        compare_form = CompareProductsForm(request.POST)
        if form.is_valid():
            cd = compare_form.cleaned_data
            product_1 = cd['product_1']
            product_2 = cd['product_2']
            return render(request, 'forms/compare_products.html', {'product_1':product_1, 'product_2':product_2})
    else:
        form = CompareProductsForm()
    return render(request, 'forms/compare_products.html', {'form':form})
