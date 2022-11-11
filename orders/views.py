from ast import Or, Try
import datetime 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from orders.forms import OredrForm
from store.models import Product
from .models import Order, OrderProduct, Payment
import json
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from carts.views import _cart_id

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



    
    


def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get( is_ordered=False, order_number=body['orderID'])
   
    if not request.user.is_anonymous :
        payment = Payment(
            
            user= request.user,
            payment_id = body['transId'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status=body['status'],

        )

        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        #Move the cart items to order products

        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.payment = payment
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
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        #send order number and trans id back senData 
        data = {
            'order_number': order.order_number,
            'transId': payment.payment_id
        }

        return JsonResponse(data)
    else:
        
        payment = Payment(
            
            
            payment_id = body['transId'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status=body['status'],

        )

        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        #Move the cart items to order products
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            orderProduct = OrderProduct()
            
            orderProduct.order_id = order.id
            orderProduct.payment = payment
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

        data = {
            'order_number': order.order_number,
            'transId': payment.payment_id
        }
        return JsonResponse(data)
        




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
        print('i enter heeereeeeeeeeeee')
        form = OredrForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = Order()
            if not request.user.is_anonymous:
                data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
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
        payment = Payment.objects.get(payment_id = transId)

        sub_total=0

        for i in order_products:
            sub_total += i.product_price

        context = {
            'order': order,
            'order_products': order_products,
            'order_number':order_number,
            'transId' : transId,
            'payment': payment,
            'sub_total':sub_total
        }

        return render(request, 'orders/order_complete.html', context)

    except:
        return render(request, 'orders/order_complete.html')
    

