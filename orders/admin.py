from django.contrib import admin
from .models import  Order, OrderProduct
# Register your models here.


class OrederProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ['user', 'product', 'variation', 'product_price', 'quantity', 'is_ordered']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_number', 'full_name', 'phone', 'wilaya', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered' ]
    search_fields = ['order_number', 'full_name', 'phone']
    list_per_page = 20
    inlines = [OrederProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)