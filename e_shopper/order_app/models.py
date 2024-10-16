from django.db import models
from django.contrib.auth.models import User
from user_app.models import UserAddress
from cart_app.models import CartItemModel
from product_app.models import ProductModel,ProductSize
from datetime import timedelta

# Create your models here.
class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received','Received'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # updated
    status = models.CharField(max_length=20,choices=STATUS_CHOICES ,default='pending')
    
    order_date = models.DateTimeField(auto_now_add=True)    
    ordered_items = models.ManyToManyField(ProductModel, through='OrderItem')
    razorpay_order_id = models.CharField(max_length=100,null=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True)
    razorpay_signature = models.CharField(max_length=100,null=True)
    # new field
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES, default='pending')
    shipping_cost = models.DecimalField(max_digits=10,decimal_places=2,default=100.00)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    @property
    def expected_delivery_date(self):
        return self.order_date + timedelta(weeks=1)
    
class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(ProductSize,on_delete=models.CASCADE,null=True,blank=True)
    
    @property
    def subtotal(self):
        return self.quantity * self.price