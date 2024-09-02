from django import forms
from .models import *

# Create your forms here

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username','email','password']

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            if len(password) < 8:
                raise forms.ValidationError('Your password is short! Your password should be 8 characters or mare than it')
            else:
                return password
            
    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if Customer.objects.filter(email=email).exists():
                raise forms.ValidationError('This email already exists!')
            else:
                return email


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserLogin
        fields = ['username','password']

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            if len(password) < 8:
                raise forms.ValidationError('Your password is short!')
            else:
                return password


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['customer','quantity','phone']
