from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.search import *

# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
     
    
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", 'DRAFT'
        PUBLISHED = "PB", 'PUBLISHED'
        REJECTED = "RJ", 'REJECTED'

    #relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_posts", verbose_name='نویسنده')
    #data fields
    title = models.CharField(max_length=250, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=250, verbose_name='اسلاگ')
    #date
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #choise fields
    status = models.CharField(max_length=2, default=Status.PUBLISHED, choices=Status.choices, verbose_name='وضعیت')
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')
    vahed = models.CharField(max_length=250, verbose_name='واحد اندازه گیری')
    video = models.FileField(upload_to='static/videos', verbose_name='ویدیو', default=None)

    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])
    
class Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(max_length=250, verbose_name='موضوع')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'



    def __str__(self):
        return self.name
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=True, verbose_name='وضعیت')


    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'


    def __str__(self):
        return f'{self.name} : {self.post}'
    
    
    def get_absolute_url_5(self):
        return reverse("blog:edit_comment", args=[self.post.id, self.id])
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='likes', verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        ordering = ['updated']
        indexes = [
            models.Index(fields=['updated'])
        ]
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'


    def __str__(self):
        return f'{self.name} : {self.post}'
    
class Favorits(models.Model):
    post = models.ForeignKey(Post, related_name = 'favorites', on_delete=models.CASCADE, verbose_name='پست')
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='کاربر', default=2)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        ordering = ['updated']
        indexes = [
            models.Index(fields=['updated'])
        ]

        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'


    def __str__(self) :
        return f'{self.post}'


    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.post.id])
    
class Login(models.Model):
    password = models.CharField(max_length=200, verbose_name='پسوورد')
    username = models.CharField(max_length=300 ,verbose_name='اسم کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=False, verbose_name='فعالیت')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'لاگ این'
        verbose_name_plural = 'لاگ این ها'

    def __str__(self):
        return f'{self.password}'
    
    def get_absolute_url_2(self):
        return reverse("blog:logout", args=[self.id])
    
    
class Profile(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    phone_number = models.IntegerField(verbose_name='شماره موبایل')
    age = models.IntegerField(verbose_name='سن')
    bio = models.CharField(max_length=300, verbose_name='بیو')
    image = models.ImageField(upload_to='static/images', verbose_name='تصویر', default='static/images/tech.jpg')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=True, verbose_name='فعالیت')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name='پروفایل'
        verbose_name_plural='پروفایل ها'

    def __str__(self):
        return f'{self.full_name}'
    

    def get_absolute_url_3(self):
        return reverse("blog:profile_detail", args=[self.id])
    
    
    def get_absolute_url_4(self):
        return reverse("blog:edit_profile", args=[self.id])
    
