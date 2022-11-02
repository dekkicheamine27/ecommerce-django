from unicodedata import category
from django.shortcuts import render, get_object_or_404
from store.models import Product, Variation
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,  Paginator, PageNotAnInteger
from django.db.models import Q

# Create your views here.

def store(request,category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category = category,is_available = True)
    
    else:
        products = Product.objects.all().filter(is_available = True)
        
    
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    products_count = products.count()
    return render(request, 'store/store.html',{
        'products': paged_products,
        'products_count': products_count
    })

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.all().get(category__slug= category_slug,slug = product_slug)
        in_cart= CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()
       
    except Exception as e:
        raise e
    
    return render(request, 'store/product_detail.html',{
        'product': product,
        'in_cart' : in_cart,
        
    } )


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains = keyword) | Q(description__icontains = keyword))
            products_count = products.count()
    return render(request, 'store/store.html', {
        'products': products,
        'products_count': products_count
    })
