from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, CartProduct
from .forms import CartAddProductForm, CartProductPayForm
from shop.models import Product


@login_required
def cart_list(request):
    try:
        cart = Cart.objects.get(owner=request.user)
    except Cart.DoesNotExist:
        cart = Cart(owner=request.user)
        cart.save()
    products = CartProduct.objects.filter(cart=cart, now_in_cart=True)
    return render(request, 'cart/list.html', {'products': products})


@login_required
@require_POST
def cart_add(request, product_id):
    try:
        cart = Cart.objects.get(owner=request.user)
    except Cart.DoesNotExist:
        cart = Cart(owner=request.user)
        cart.save()
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        try:
            cartproduct = CartProduct.objects.get(cart=cart, product=product, now_in_cart=True)
        except CartProduct.DoesNotExist:
            cartproduct = CartProduct(cart=cart, product=product, price=product.price, quantity=0, now_in_cart=True)
        if cd['override']:
            cartproduct.quantity = cd['quantity']
        else:
            cartproduct.quantity += cd['quantity']
        cartproduct.save()
        if cd['override']:
            slug = cartproduct.product.slug
            messages.success(request, "Вы успешно изменили количество товара в корзине")
            return redirect('cart:cart_detail', pk=cartproduct.id, slug=slug)
        else:
            messages.success(request, "Вы успешно добавили товар в корзину")
    else:
        messages.error(request, "Не удалось добавить товар в корзину, скорее всего, вы неправильно заполнили форму")
    return redirect('cart:cart_list')


@login_required
def cart_detail(request, pk, slug):
    cart = get_object_or_404(Cart, owner=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, now_in_cart=True, id=pk)
    overall_cost = cart_product.quantity * cart_product.price
    change_quantity_form = CartAddProductForm(initial={'quantity': cart_product.quantity, 'override': True})
    pay_form = CartProductPayForm()
    return render(request, 'cart/product_detail.html',
                  {'cart_product': cart_product, 'quantity_form': change_quantity_form,
                   'overall_cost': overall_cost, 'pay_form': pay_form})


@login_required
@require_POST
def cart_remove(request, pk):
    cart = get_object_or_404(Cart, owner=request.user)
    get_object_or_404(CartProduct, cart=cart, now_in_cart=True, id=pk).delete()
    messages.success(request, "Вы успешно удалили товар из корзины")
    return redirect('cart:cart_list')
