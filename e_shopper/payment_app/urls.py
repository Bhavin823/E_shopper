# dj_razorpay/urls.py

from django.contrib import admin
from django.urls import path
from payment_app import views

app_name = 'payment_app'

urlpatterns = [
    # payment intialize
    path("payment/<int:order_id>/", views.order_payment, name="payment"),
    
    # after payment 
    path("callback/", views.callback, name="callback"),
    
    # after payment status call 
    path('payment_success_page/',views.payment_success_page,name='payment_success_page'),
    
]
