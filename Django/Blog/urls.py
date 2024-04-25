from django.urls import path 
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<pk>', views.post_detail, name='post_detail'),
    path('posts/<post_id>/comment', views.post_comment, name='post_comment'),
    path('ticket', views.ticket, name='ticket'),
    path('postform', views.post_form, name='postform'),
    path('login/', views.login_form, name='login'),
    path('counter/', views.counter, name='counter'),
    path('counter/counter', views.counter, name='counter'),
    path('translation/', views.translate, name='translate'),
    path('profile/', views.profile, name='profile'),
    path('posts/<int:id>/delete_post', views.delete_post, name='delete_post'),
    path('posts/<int:id>/edit_post', views.edit_post, name='edit_post'),
    path('posts/<int:id>/edit_comment', views.edit_comment, name='edit_comment'),
    path('posts/<int:id>/delete_comment', views.delete_comment, name='delete_comment'),
    path('fl_testing/', views.fl_testing, name='fl_testing'),
]
