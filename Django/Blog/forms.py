class PostForm(forms.Form):
    VAHED_CHOICES=(
        ('ثانیه','ثانیه'),
        ('دقیقه','دقیقه'),
        ('ساعت','ساعت'),
    )
    author = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'نویسنده', 'class':'auth'}))
    title = forms.CharField(max_length=350, widget=forms.TextInput(attrs={'placeholder':'عنوان', 'style':'height:50px;'}))
    description = forms.CharField(widget=forms.Textarea)
    reading_time = forms.IntegerField(max_value=999)
    vahed = forms.ChoiceField(choices=VAHED_CHOICES)
