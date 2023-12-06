from django.contrib import admin
from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_checked', 'accepted', 'paid', 'created', 'updated']
    list_filter = ['is_checked', 'user', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
