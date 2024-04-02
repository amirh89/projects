from django.contrib import admin
from .models import *
# Register your models here.

admin.sites.AdminSite.site_header = 'پنل مدیریت جنگو'
admin.sites.AdminSite.site_title = 'پنل'
admin.sites.AdminSite.index_title = 'پنل مدیریت'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','publish','author','status','vahed']
    ordering = ['title','publish']
    list_filter = ['status','author','publish']
    search_fields = ['title','description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug' : ['title']}
    list_editable = ['status']
    #list_display_links = ['author']
