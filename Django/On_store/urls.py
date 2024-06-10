from django.urls import path
from on_store import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('product/', views.product, name='product'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('product_list/<pk>/', views.product_detail, name='product_detail'),
    path('product_list/<pk>/order/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('search_product/', views.search_bar, name='search_bar'),
    path('product_list/<pk>/comment/', views.product_comment, name='product_comment'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
