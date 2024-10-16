# dj_razorpay/urls.py

from django.contrib import admin
from django.urls import path
from payment_app import views

app_name = 'payment_app'

urlpatterns = [
    
	# path('initialize_razorpay/<int:order_id>/', views.initialize_razorpay, name='initialize_razorpay'),
    # path('razorpay_payment_success/', views.razorpay_payment_success, name='razorpay_payment_success'),
    
    path('payment_success_page/',views.payment_success_page,name='payment_success_page'),
    # path('payment_faliure_page/',views.payment_failure_page,name='payment_failure_page'),


    # new flow 
    path("payment/<int:order_id>/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),

]
