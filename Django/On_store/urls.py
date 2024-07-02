from django.urls import path
from on_store import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('customer_detail/<pk>/logout/', views.logout, name='logout'),
    path('customer_detail/<pk>/', views.customer_detail, name='customer_detail'),
    path('customer_detail/<pk>/edit_profile/', views.edit_profile, name='edit_profile'),
    path('product/', views.product, name='product'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('product_list/<pk>/', views.product_detail, name='product_detail'),
    path('product_list/<pk>/comment/', views.product_comment, name='product_comment'),
    path('product_list/<pk>/delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('products/<int:id>/', views.products_of_categories, name='products_of_categories'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('product_list/<pk>/order/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/delete_all/', views.delete_all_products_from_cart, name='delete_products_from_cart'),
    path('favorite_list/', views.FavoritesList.as_view(), name='favorite_list'),
    path('product_list/<pk>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('favorite_list/remove/<int:id>/', views.remove_product_from_favorite_list, name='remove_product_from_favorite_list'),
    path('search_product/', views.search_bar, name='search_bar'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
