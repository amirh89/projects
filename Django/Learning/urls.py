from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'learning'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),
    path('welcome/', welcome, name='welcome'),
    path('profile/<pk>/', profile, name='profile'),
    path('profile/<pk>/logout/', logout, name='logout'),
    path('pack_list/', PackList.as_view(), name='pack_list'),
    path('pack_list/pack_detail/<pk>/', package_detail, name='package_detail'),
    path('pack_list/pack_detail/<pk>/edit_pack/', edit_pack, name='edit_pack'),
    path('pack_detail/<pk>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', CartList.as_view(), name='cart_list'),
    path('add_pack/', AddPack.as_view(), name='add_pack'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
