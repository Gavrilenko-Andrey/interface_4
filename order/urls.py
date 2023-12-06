from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create_order/<int:pk>/', views.create_order, name='create_order'),
    path('process_order/<int:order_id>/<int:accepted>/', views.process_order, name='process_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('', views.view_orders, name='view_orders'),
]
