from django.db import models
from django.urls import reverse

# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(default=None)
    password = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.username
    
class UserLogin(models.Model):
    username = models.CharField(max_length=1111)
    password = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'UserLogin'
        verbose_name_plural = 'UsersLogin'

    def __str__(self):
        return self.username
    
class LearningPackage(models.Model):
    class Ed(models.TextChoices):
        LANGUAGE = 'LANGUAGE','LANGUAGE'
        COMPUTER = 'COMPUTER','COMPUTER'
        ECONOMICS = 'ECONOMICS','ECONOMICS'
    name = models.CharField(max_length=300)
    description = models.TextField()
    author = models.CharField(max_length=300, default='')
    category = models.CharField(max_length=20, choices=Ed.choices, default=Ed.LANGUAGE)
    image = models.ImageField(upload_to='static/image', default=None)
    video = models.FileField(upload_to='static/video', default=None)
    price_with_discount = models.IntegerField()

    class Meta:
        verbose_name = 'LearningPackage'
        verbose_name_plural = 'LearningPackages'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("learning:package_detail", args=[self.pk])
    
class Cart(models.Model):
    package = models.ForeignKey(LearningPackage, on_delete=models.CASCADE, default='')
    customer = models.ForeignKey(UserLogin, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    phone = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f'{self.package} by {self.customer}'
