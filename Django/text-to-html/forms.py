from django import forms
from ckeditor.widgets import CKEditorWidget

class TextConvertorForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget(), label='')
