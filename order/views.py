from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from cart.models import CartProduct, Cart
from .models import Order, OrderItem
from cart.forms import CartProductPayForm


@login_required
@require_POST
def create_order(request, pk):
    cart = get_object_or_404(Cart, owner=request.user)
    cart_product = get_object_or_404(CartProduct, id=pk, now_in_cart=True, cart=cart)
    form = CartProductPayForm(request.POST)
    if form.is_valid():

        order = Order(user=request.user, owner=cart_product.product.owner)
        order.save()
        order_item = OrderItem(order=order, product=cart_product.product,
                               price=cart_product.price, quantity=cart_product.quantity)
        order_item.save()
        cart_product.now_in_cart = False
        cart_product.save()
        messages.success(request, "Вы успешно создали заказ")
        return redirect('cart:cart_list')
    else:
        messages.error(request, "Форма была заполнена неверно, заказ создать не удалось")
        return redirect('cart:cart_detail', cart_product.id, cart_product.product.slug)


@login_required
def view_orders(request):
    # orders = Order.objects.filter(owner=request.user)
    orders = Order.objects.filter(items__product__owner=request.user)
    order_items = OrderItem.objects.filter(order__in=orders).order_by(F('order__created').desc())
    return render(request, 'order/orders.html', {"order_items": order_items})


@login_required
@require_POST
def process_order(request, order_id, accepted):
    order = get_object_or_404(Order, items__product__owner=request.user, id=order_id)
    if order.is_checked:
        return redirect('order:view_orders')
    if accepted:
        order.accepted = True

    else:
        order.accepted = False
    order.is_checked = True
    order.save()
    messages.success(request, "Вы успешно обработали заказ")
    return redirect('order:view_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    order_items = OrderItem.objects.filter(order__in=orders).order_by(F('order__created').desc())
    return render(request, 'order/my_orders.html', {"order_items": order_items})


