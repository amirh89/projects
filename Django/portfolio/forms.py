from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

# Create your forms here.

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(min_length=4, required=True)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=4, required=True)
    password_2 = forms.CharField(min_length=4, required=True, label='Password(again)')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone']


    def clean_password_2(self):
        cd = self.cleaned_data
        if cd:
            if cd['password_2'] != cd['password']:
                raise forms.ValidationError('The passwords are not same!')
            else:
                return cd['password_2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','date_of_birth','bio','job','phone','photo']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['category','title','description','image','film','audio','author','time_to_read']

    image = forms.ImageField(required=False)
    film = forms.FileField(required=False)
    audio = forms.FileField(required=False)


class SearchForm(forms.Form):
    query = forms.CharField()
