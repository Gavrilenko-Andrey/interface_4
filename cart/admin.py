from django.contrib import admin
from .models import Cart, CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['owner', 'created']


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'price', 'quantity', 'created', 'updated', 'now_in_cart']
    list_filter = ['now_in_cart', 'cart', 'product', 'created', 'updated']
    list_editable = ['price', 'quantity', 'now_in_cart']
