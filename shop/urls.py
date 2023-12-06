from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('my-products/', views.list_my_products, name='my_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-product/<int:pk>/<slug:slug>/', views.add_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),


]
