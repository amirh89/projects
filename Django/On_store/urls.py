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
    path('product_list/<pk>/comment/', views.product_comment, name='product_comment'),
    path('product_list/<pk>/allowance/', views.allowance, name='product_allowance'),
    path('product_list/<int:id>/delete_allowance/', views.delete_allowance, name='delete_allowance'),
    path('products/<int:id>/', views.products_of_categories, name='products_of_categories'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('product_list/<pk>/order/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/delete_all/', views.delete_all_products_from_cart, name='delete_products_from_cart'),
    path('search_product/', views.search_bar, name='search_bar'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
