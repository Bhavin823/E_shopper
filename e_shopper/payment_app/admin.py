from django.contrib import admin
from .models import RazorpayOrder,RazorpayPayment

# Register your models here.
admin.site.register(RazorpayOrder)
admin.site.register(RazorpayPayment)
