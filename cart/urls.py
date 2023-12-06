from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [

    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('list/', views.cart_list, name='cart_list'),
    path('<int:pk>/<slug:slug>/', views.cart_detail, name='cart_detail'),
    path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
]
