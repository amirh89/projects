from django.urls import path
from .views import *

app_name = 'book'
urlpatterns = [
    path('', convert_text_to_html, name='convertor_view')
]
