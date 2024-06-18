from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','created','updated']
    list_filter = ['first_name','last_name']
    search_fields = ['phone','email']
    list_editable = ['email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']
    list_filter = ['name','category']
    search_fields = ['price']
    list_editable = ['category']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','customer','price','quantity']
    list_filter = ['price','status']
    search_fields = ['price']
    list_editable = ['quantity']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','name','created']
    list_filter = ['created','updated']
    search_fields = ['text']

@admin.register(Allowance)
class AllowanceAdmin(admin.ModelAdmin):
    list_display = ['product','amount','date']
    list_filter = ['date']
    search_fields = ['description']
