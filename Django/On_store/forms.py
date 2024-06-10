from django import forms
from .models import *

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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','category','description','image']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','quantity','price','address','phone']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=260)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','text']
