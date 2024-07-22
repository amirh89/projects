from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import datetime
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=70)
    picture = models.ImageField(upload_to='static/images', default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:products_of_categories", args=[self.id])
    

class Customer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
    
    def __str__(self):
        return self.last_name
    
    def get_absolute_url(self):
        return reverse("store:customer_detail", args=[self.id])
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default=1, related_name="products")
    description = models.CharField(max_length=300, default='', null=True, blank=True)
    image = models.ImageField(upload_to='static/images', default=None, null=True, blank=True)
    allowance_amount = models.IntegerField(default=0)
    text = models.TextField(default="")
     
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f"{self.name} : {self.category}"
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.id])
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=400, default='', blank=True)
    phone = models.IntegerField(default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.product}'

    
class Search(models.Model):
    query = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=300)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'{self.name} : {self.product}'


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'

    def __str__(self):
        return f"{self.product}"
