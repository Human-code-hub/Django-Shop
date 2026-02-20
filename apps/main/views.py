from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
# from cart.forms import CartAddProductForm


def popular_list(request):
    products = Product.objects.all()
    return render(request, "main/index/index.html", {'products':products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # cart_product_form = CartAddProductForm
    return render(request, "main/product/detail.html", {'product': product})

def product_list(request, category_slug=None):
    page_number = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().select_related("category")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, "main/product/list.html", {
            "category": category,
            "categories": categories,
            "products": page_obj.object_list,
            "page_obj": page_obj,
            "category_slug": category_slug,
        },)
