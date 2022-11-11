from django.urls import path
from . import views


urlpatterns = [
    
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('paymentAfterReceiving/<int:order_number>', views.paymentAfterReceiving, name='paymentAfterReceiving'),
    path('order_complete/', views.order_complete, name='order_complete'),
    
] 