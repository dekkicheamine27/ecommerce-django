from django.urls import path
from . import views


urlpatterns = [
    
    path('place_single_product_order/<int:product_id>', views.place_single_product_order, name='place_single_product_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('paymentAfterReceiving/<int:order_number>', views.paymentAfterReceiving, name='paymentAfterReceiving'),
    path('paymentsingleProduct/<int:order_number>/<int:product_id>', views.paymentsingleProduct, name='paymentsingleProduct'),
    path('order_complete/', views.order_complete, name='order_complete'),
    
] 