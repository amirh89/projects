from django import forms
from .models import Comment
from django.utils import timezone
from django.contrib.auth.models import User


class TicketForm(forms.Form):
    SUBJECT_CHOICES=(
        ('پیشنهاد','پیشنهاد'),
        ('انتقاد','انتقاد'),
        ('گزارش','گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder':'نام',
                                                                                        'style':'height:60px;', 'class':'name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل', 'style':'width:345px', 'class':'ti_email'}))
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('!شماره تلفن عددی نیست')
            else:
                return phone
            
class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name)<3:
                raise forms.ValidationError('!نام کوتاه است')
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name','body']
        widgets = {
            'body':forms.TextInput(attrs={
                'placeholder':'متن',
                'class':'cm_body'
            }),
            'name':forms.TextInput(attrs={
                'placeholder':'نام',
                'class':'cm_name'
            })
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author','title','description','reading_time','vahed']

class LoginForm(forms.Form):
    password = forms.IntegerField(max_value=999999, required=True, widget=forms.TextInput(attrs={'placeholder':'باید شش رقمی باشد','class':'psw'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'usn'}))

    def clean_username(self):
        usn = self.cleaned_data['username']
        if usn:
            if usn.isnumeric():
                raise forms.ValidationError('!اسم کاربر حروفی نیست')
            else:
                return usn
            
class ProfileForm(forms.Form):
    full_name = forms.CharField(required=True, max_length=200)
    phone_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder':'با 09 شروع کنید'}))
    age = forms.IntegerField(required=True)
    bio = forms.CharField(required=False)
