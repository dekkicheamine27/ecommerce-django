from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.


class OrederProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_number', 'full_name', 'phone', 'email', 'wilaya', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered' ]
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrederProductInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)