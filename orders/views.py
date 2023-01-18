
import datetime 
from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
from orders.forms import OredrForm
from store.models import Product, Variation
from .models import Order, OrderProduct
from django.core.exceptions import ObjectDoesNotExist

from django.template.loader import render_to_string
from carts.views import _cart_id



def paymentsingleProduct(request, order_number, product_id):
    product = Product.objects.get(id=product_id)
    try:
        order = Order.objects.get( is_ordered=False, order_number=order_number)
    except:
        return redirect('store')
    order.is_ordered = True
    order.save()

    if not request.user.is_anonymous :
        cart_items = CartItem.objects.filter(user=request.user, product = product)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.user_id = request.user.id
            orderProduct.product_id = item.product_id
            orderProduct.product_price = item.product.price
            orderProduct.quantity = item.quantity
            orderProduct.is_ordered = True
            
            
            
            orderProduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variation.all()
            orderProduct = OrderProduct.objects.get(id=orderProduct.id)
            orderProduct.variation.set(product_variation)

            orderProduct.save()

            #reduce quantity

            product = Product.objects.get(id=item.product.id)
            product.stock  -= item.quantity  
            product.save()
        

        #clear cart 

        CartItem.objects.filter(user=request.user).delete()

        #send emai to costumer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_recived_email.html', {
            'user': request.user,
            'order': order
        })
        """ to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send() """

        #send order number and trans id back senData 
        order_products = OrderProduct.objects.filter(order__id = order.id)

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order_number': order.order_number,
            'order_products': order_products,
            'order': order,
            'sub_total': sub_total

            
        }
        return render(request, 'orders/order_complete_without_paying.html', context)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.product_id = item.product_id
            orderProduct.product_price = item.product.price
            orderProduct.quantity = item.quantity
            orderProduct.is_ordered = True
            
            
            
            orderProduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variation.all()
            orderProduct = OrderProduct.objects.get(id=orderProduct.id)
            orderProduct.variation.set(product_variation)

            orderProduct.save()

            #reduce quantity

            product = Product.objects.get(id=item.product.id)
            product.stock  -= item.quantity  
            product.save()
        

        #clear cart 
        
        CartItem.objects.filter(cart=cart).delete()

        order_products = OrderProduct.objects.filter(order__id = order.id)

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order_number': order.order_number,
            'order_products': order_products,
            'order': order,
            'sub_total': sub_total

            
        }
        return render(request, 'orders/order_complete_without_paying.html', context)








# Create your views here.
def paymentAfterReceiving(request, order_number):
    order = Order.objects.get( is_ordered=False, order_number=order_number)
    order.is_ordered = True
    order.save()

    if not request.user.is_anonymous :
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.user_id = request.user.id
            orderProduct.product_id = item.product_id
            orderProduct.product_price = item.product.price
            orderProduct.quantity = item.quantity
            orderProduct.is_ordered = True
            
            
            
            orderProduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variation.all()
            orderProduct = OrderProduct.objects.get(id=orderProduct.id)
            orderProduct.variation.set(product_variation)

            orderProduct.save()

            #reduce quantity

            product = Product.objects.get(id=item.product.id)
            product.stock  -= item.quantity  
            product.save()
        

        #clear cart 

        CartItem.objects.filter(user=request.user).delete()

        #send emai to costumer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_recived_email.html', {
            'user': request.user,
            'order': order
        })
        """ to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send() """

        #send order number and trans id back senData 
        order_products = OrderProduct.objects.filter(order__id = order.id)

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order_number': order.order_number,
            'order_products': order_products,
            'order': order,
            'sub_total': sub_total

            
        }
        return render(request, 'orders/order_complete_without_paying.html', context)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.product_id = item.product_id
            orderProduct.product_price = item.product.price
            orderProduct.quantity = item.quantity
            orderProduct.is_ordered = True
            
            
            
            orderProduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variation.all()
            orderProduct = OrderProduct.objects.get(id=orderProduct.id)
            orderProduct.variation.set(product_variation)

            orderProduct.save()

            #reduce quantity

            product = Product.objects.get(id=item.product.id)
            product.stock  -= item.quantity  
            product.save()
        

        #clear cart 
        
        CartItem.objects.filter(cart=cart).delete()

        order_products = OrderProduct.objects.filter(order__id = order.id)

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order_number': order.order_number,
            'order_products': order_products,
            'order': order,
            'sub_total': sub_total

            
        }
        return render(request, 'orders/order_complete_without_paying.html', context)




    
def place_single_product_order(request, product_id, total=0, quantity=0):


    current_user = request.user
    product = Product.objects.get(id=product_id)
    # get the product
    product_variation = []
    # if the user is authenticated
    if current_user.is_authenticated:

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value, )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )

        cart.save()


        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
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
                item = CartItem.objects.get(product=product, id=id_item)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()

                    item.variation.add(*product_variation)

                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                cart=cart,
                quantity=1
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                for item in product_variation:
                    cart_item.variation.add(item)
            cart_item.save()
        
    # else the user is not authenticated
    else:

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value, )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )

        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
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
                item = CartItem.objects.get(product=product, id=id_item)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()

                    item.variation.add(*product_variation)

                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                for item in product_variation:
                    cart_item.variation.add(item)
            cart_item.save()
    
    


    product = Product.objects.get(id=product_id)
    if request.user.is_anonymous :
       cart = Cart.objects.get(cart_id=_cart_id(request))
       cart_items = CartItem.objects.all().filter(product = product, cart=cart, is_active=True)
       cart_count = cart_items.count()
       if cart_count <=0:
          return redirect('store')
    else:
        cart_items = CartItem.objects.filter(product = product, user = current_user)
        cart_count = cart_items.count()
        if cart_count <=0:
            return redirect('store')
    

    tax = 0
    grand_total = 0

    for item in cart_items:
            total += (item.quantity * item.product.price)
            quantity += item.quantity

    tax = (2*total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        
        form = OredrForm(request.POST)
        if form.is_valid():
            data = Order()
            if not request.user.is_anonymous:
                data.user = current_user
            data.full_name = form.cleaned_data['full_name']
            
            data.phone = form.cleaned_data['phone']
            data.wilaya = form.cleaned_data['wilaya']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))

            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = str(current_date) + str(data.id)
            data.order_number = order_number
            data.save()
            if not request.user.is_anonymous:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            else:
                order = Order.objects.get( is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'product': product,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

            return render(request, 'orders/single_product_payment.html', context)
        return redirect('store')
    else:
        
        return redirect('store')
        






   







def place_order(request, total=0, quantity=0):
    current_user = request.user

    if request.user.is_anonymous :
       cart = Cart.objects.get(cart_id=_cart_id(request))
       cart_items = CartItem.objects.all().filter(cart=cart, is_active=True)
       cart_count = cart_items.count()
       if cart_count <=0:
          return redirect('store')
    else:
        cart_items = CartItem.objects.filter(user = current_user)
        cart_count = cart_items.count()
        if cart_count <=0:
            return redirect('store')
    

    tax = 0
    grand_total = 0

    for item in cart_items:
            total += (item.quantity * item.product.price)
            quantity += item.quantity

    tax = (2*total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        
        form = OredrForm(request.POST)
        if form.is_valid():
            data = Order()
            if not request.user.is_anonymous:
                data.user = current_user
            data.full_name = form.cleaned_data['full_name']
            
            data.phone = form.cleaned_data['phone']
            data.wilaya = form.cleaned_data['wilaya']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))

            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = str(current_date) + str(data.id)
            data.order_number = order_number
            data.save()
            if not request.user.is_anonymous:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            else:
                order = Order.objects.get( is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

            return render(request, 'orders/payment.html', context)
        return redirect('checkout')
    else:
        
        return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
 
    transId = request.GET.get('paymentId')
 

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_products = OrderProduct.objects.filter(order__id = order.id)
        

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order': order,
            'order_products': order_products,
            'order_number':order_number,
            'transId' : transId,
            'sub_total':sub_total
        }

        return render(request, 'orders/order_complete.html', context)

    except:
        return render(request, 'orders/order_complete.html')
    

