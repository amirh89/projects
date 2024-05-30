from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
    

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


    def register(self):
        self.save()
    

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        
        return False
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default=1)
    description = models.CharField(max_length=300, default='', null=True, blank=True)
    imagge = models.ImageField(upload_to='static/iamges', default=None)
     
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
        
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
     
    def placeOrder(self):
        self.save()
    
    @staticmethod
    def get_order_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
