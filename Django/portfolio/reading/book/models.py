from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from .saving_media import *

# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="static/images", blank=True, null=True)
    job = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Category(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='static/images', default=None)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Object(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='objs')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images', default=None, validators=[FileExtensionValidator(['png','jpg'])], null=True, blank=True)
    film = models.FileField(upload_to='static/movie', default=None, validators=[FileExtensionValidator(['mp4'])], null=True, blank=True)
    audio = models.FileField(upload_to='static/audio', default=None, validators=[FileExtensionValidator(['mp3','wav'])], null=True, blank=True)
    author = models.CharField(max_length=500)
    time_to_read = models.PositiveIntegerField()
    like = models.ManyToManyField(User, related_name='liked_objects', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    saved_by = models.ManyToManyField(User, related_name='saved_objects', blank=True)
    total_saves = models.PositiveIntegerField(default=0)
    object_hash = models.CharField(max_length=32, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'

    def get_absolute_url(self):
        return reverse("hobby:object_detail", args=[self.pk])
    
    def save_image(self, *args, **kwargs):
        self.object_hash = generate_md5(self.image)

        if not Object.objects.filter(object_hash=self.object_hash).exists():
            super().save(*args, **kwargs)
    

class Comments(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=300)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'