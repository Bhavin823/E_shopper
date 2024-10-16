from django.contrib import admin
from order_app.models import OrderModel,OrderItem

# Register your models here.
@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','shipping_address',
                    'payment_type','total_amount',
                    'status','payment_status',
                    'shipping_cost','tracking_number',
                    'order_date','razorpay_payment_id',
                    'razorpay_order_id','razorpay_signature']
    
    list_filter = ('status','payment_type', 'payment_status', 'order_date')

    list_editable = ['status']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','product','size','quantity','price']
