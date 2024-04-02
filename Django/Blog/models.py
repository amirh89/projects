from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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
