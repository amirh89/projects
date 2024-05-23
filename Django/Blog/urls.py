from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
    #home
    path('', views.index, name='index'),
    #post
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/favorites', views.FavoritePostsView.as_view(), name='favorites_list'),
    path('posts/favorites/form/', views.add_to_favorites, name='favorites'),
    path('posts/favorites/<int:id>/remove/', views.remove_from_favorites, name='re_favorites'),
    path('posts/<pk>', views.post_detail, name='post_detail'),
    path('posts/<pk>/delete_post', views.delete_post, name='delete_post'),
    path('posts/<int:id>/edit_post', views.edit_post, name='edit_post'),
    path('posts/<post_id>/comment', views.post_comment, name='post_comment'),
    path('posts/<int:id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('posts/<int:id>/delete_comment', views.delete_comment, name='delete_comment'),
    path('posts/<post_id>/like', views.post_like, name='post_like'),
    #form
    path('ticket', views.ticket, name='ticket'),
    path('postform', views.post_form, name='postform'),
    #log
    path('login/', views.login_form, name='login'),
    path('<int:id>/logout/', views.logout_form, name='logout'),
    #profile
    path('profile/' ,views.profile, name='profile'),
    path('<pk>/profile_detail/', views.profile_detail, name='profile_detail'),
    path('<int:id>/profile_detail/edit_profile/', views.edit_profile, name='edit_profile'),
    path('<pk>/profile_detail/delete_profile', views.delete_profile, name='delete_profile'),
    #python
    path('fl_testing/', views.fl_testing, name='fl_testing'),
    path('counter/', views.counter, name='counter'),
    path('counter/counter', views.counter, name='counter'),
    path('translation/', views.translate, name='translate'),
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
