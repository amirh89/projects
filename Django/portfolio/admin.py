from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields':('date_of_birth', 'bio', 'job', 'phone')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ['title','total_likes','total_saves']
    search_fields = ['title']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['object']
    search_fields = ['name','body']
