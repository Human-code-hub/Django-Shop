from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
# from cart.forms import CartAddProductForm


def popular_list(request):
    products = Product.objects.filter(available=True)
    return render(request, "main/index/index.html", {'products':products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    # cart_product_form = CartAddProductForm
    return render(request, "main/product/detail.html", {'product': product})

def product_list(request, category_slug=None):
    page_number = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 10)
    obj_page = paginator.get_page(page_number)

    return render(request, "main/product/list.html", {'category':category, 'categories':categories, 'obj_page': obj_page, 'category_slug':category_slug})
