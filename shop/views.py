from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.decorators.http import require_POST
from unidecode import unidecode
from .models import Category, Product
from .forms import AddProductForm, SearchForm
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    form = SearchForm()
    query = None
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('name', weight='A', config='russian') + \
                SearchVector('description', weight='C', config='russian')
            search_query = SearchQuery(query)
            products = products.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
                search=search_query).order_by('-rank')
    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'form': form,
                   'query': query}
                  )


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug, available=True)
    form = CartAddProductForm(initial={'quantity': 1})
    return render(request, 'shop/product/detail.html', {'product': product, 'addproductform': form})


@login_required
def add_product(request, pk=None, slug=None):
    if pk:
        product = get_object_or_404(Product, id=pk, available=True)
    else:
        product = None
    if request.method == 'POST':
        if pk:
            product_add_form = AddProductForm(data=request.POST, files=request.FILES, instance=product)
            edit = True
        else:
            product_add_form = AddProductForm(request.POST, request.FILES)
            edit = False
        if product_add_form.is_valid():
            new_product = product_add_form.save(commit=False)
            new_product.slug = slugify(unidecode(new_product.name))
            new_product.owner = request.user
            new_product.save()
            messages.success(request, "Вы успешно добавили товар")
            return redirect('shop:my_products')
        else:
            messages.error(
                request, "При добавлении товара произошла ошибка, скорее всего, Вы неправильно заполнили форму")
    else:
        if pk:
            product_add_form = AddProductForm(instance=product)
            edit = True
        else:
            product_add_form = AddProductForm()
            edit = False
    return render(request, 'shop/add_product.html',
                  {'add_product_form': product_add_form, 'edit': edit, 'product': product})


@login_required
@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk, available=True)
    product.available = False
    product.save()
    messages.success(request, "Вы успешно удалили товар")
    return redirect('shop:my_products')


@login_required
def list_my_products(request):
    my_products = Product.objects.filter(owner=request.user, available=True).order_by('-created')
    return render(request, 'shop/my_products.html', {'my_products': my_products})
