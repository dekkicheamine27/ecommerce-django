from ast import Try
from base64 import urlsafe_b64encode
from email import message
from email.policy import default
from http.client import HTTPResponse
import imp
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from accounts.models import Account
from carts.models import Cart, CartItem
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from carts.views import _cart_id
from orders.models import Order, OrderProduct
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password

            )
            user.phone = phone
            user.save()

            # Activate user
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message = render_to_string('accounts/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

           #messages.success(request, 'Thank you for registration with us, we have sent a verivication email to your email adress, please verify it!')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
    })


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    #Getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    #Get the cart items to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        existing_variation = list(existing_variation)
                        ex_var_list.append(existing_variation)
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            id_item = id[index]
                            item = CartItem.objects.get(id=id_item)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                    item.user = user
                                    item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are Logged Out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation you account is activated!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    oreders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True,)
    orders_count = oreders.count()
    context = {
        'orders': oreders,
        'orders_count': orders_count
            }
    return render(request, 'accounts/dashboard.html', context )


def forgotPassword(request):
    if request.method == 'POST':

        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            user.save()

        # Activate user
            current_site = get_current_site(request)
            mail_subject = 'Click on link to rest password'
            message = render_to_string('accounts/rest_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'we send link to your email')
            return redirect('login')
        else:
            messages.error(request, 'does not exist')
            return redirect('forgotPassword')

    else:
        form = RegistrationForm()

    return render(request, 'accounts/forgotPassword.html')


def restPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please rest your password')
        return redirect('restPasswordPage')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('login')


def restPasswordPage(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)

            user.set_password(password)

            user.save()

            messages.success(request, 'Password rest successful!')
            return redirect('login')
        else:
            messages.error(request, 'password do not match!')
            return redirect('restPasswordPage')

    else:
        return render(request, 'accounts/restPasswordPage.html')

def my_orders(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True,)
    context ={
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    print(order_detail)
    order = Order.objects.get(order_number=order_id)
    sub_total=0
    for i in order_detail:
        sub_total = i.product_price * i.quantity
    context = {
        "order_detail": order_detail,
        "order":order,
        "sub_total": sub_total
        
    }
    return render(request,'accounts/order_detail.html', context)
