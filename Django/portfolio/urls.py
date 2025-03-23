from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

# Create the urls here.

app_name = 'hobby'
urlpatterns = [
    path('', home, name='home'),

    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', log_out, name='logout'),
    path('edit_user/', edit_user, name='edit_user'),
    path('profile/', profile, name='profile'),

    path('<pk>/post_comment/', post_comment, name='post_comment'),

    path('objects_of_category/<str:name>/', objects_of_category, name='objects_of_category'),

    path('add_object/', add_object, name='add_object'),
    path('objects/', ObjectList.as_view(), name='object_list'),
    path('objects/<pk>/', object_detail, name='object_detail'),
    path('objects/<pk>/edit/', edit_object, name='edit_object'),

    path('search_object/', search_object, name='search_object'),

    path('like_object/', like_object, name='like_object'),
    path('save_object/', save_object, name='save_object'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
