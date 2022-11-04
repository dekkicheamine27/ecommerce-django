from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('restPassword/<uidb64>/<token>/', views.restPassword, name='restPassword'),
    path('restPasswordPage/', views.restPasswordPage, name='restPasswordPage'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),

] 