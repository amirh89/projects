from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'style':'height:60px;' 'width:900px;'}))
    last_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'style':'height:60px;' 'width:900px;'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'style':'height:60px;' 'width:900px;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'style':'height:60px;' 'width:900px;'}))
    password = forms.CharField(max_length=90, widget=forms.TextInput(attrs={'style':'height:60px;' 'width:900px;'}))
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('Your phone number is not numeric!')
            else:
                return phone

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','phone','email','password']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','category','description','image','allowance_amount','text']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','quantity','address','phone']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=260, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','text']


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []

class CompareProductsForm(forms.Form):
    product_1 = forms.ModelChoiceField(queryset=Product.objects.all())
    product_2 = forms.ModelChoiceField(queryset=Product.objects.all())
