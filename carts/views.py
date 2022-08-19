from ast import Return
from django.shortcuts import render, redirect, get_object_or_404
from store.models import  Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
           
            
            try:
                variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value, )
                product_variation.append(variation)
            except:
                pass

    

    try:
       cart= Cart.objects.get(cart_id = _cart_id(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product = product, cart =cart).exists()

    
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product = product, cart = cart)
        
        ex_var_list =[]
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            existing_variation = list(existing_variation)
            ex_var_list.append(existing_variation)
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            id_item = id[index]
            item = CartItem.objects.get(product = product, id=id_item)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
            if len(product_variation) > 0:
               item.variation.clear()
        
               item.variation.add(*product_variation)
            
            item.save()
            
            
        
        

        
    else:
        cart_item = CartItem.objects.create(
            product = product, 
            cart = cart,
            quantity = 1
        )
        if len(product_variation)>0:
            cart_item.variation.clear()
            for item in product_variation:
               cart_item.variation.add(item)
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id, item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=item_id)

        if cart_item.quantity>1:
          cart_item.quantity -=1
          cart_item.save()
        else:
           cart_item.delete()
        
    except:
        pass
    return redirect('cart')
    
def remove_cart_item(request, product_id, item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
       cart_item = CartItem.objects.get(product=product, cart=cart, id =item_id)
       cart_item.delete()
    except:
        pass
    return redirect('cart')

    
def cart(request, total=0, quantity=0, cart_items=None):
    try:
       tax =0 
       grand_total = 0
       cart = Cart.objects.get(cart_id = _cart_id(request) )
       cart_items = CartItem.objects.all().filter(cart = cart, is_active = True )
       total = 0
       for item in cart_items:
          total += (item.quantity * item.product.price)
          quantity += item.quantity
    
       tax = (2*total)/100
       grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    })
