from unicodedata import category
from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category

# Create your views here.

def store(request,category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category = category,is_available = True)
    
    else:
        products = Product.objects.all().filter(is_available = True)

    products_count = products.count()
    return render(request, 'store/store.html',{
        'products': products,
        'products_count': products_count
    })

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.all().get(category__slug= category_slug,slug = product_slug)
    except Exception as e:
        raise e
    return render(request, 'store/product_detail.html',{
        'product': product,
    } )
