from django.contrib import admin
from django.urls import path
from cart_app.views import *

app_name = 'cart_app'

urlpatterns = [
    # for add items in cart
    path('add_to_cart/<slug:productslug>',add_to_cart, name='add_to_cart'),
    # for cart page
    path('usercart', cartView, name='cart'),
    path('deleteitem/<int:item_id>', delete_cart_item, name='delete_cart_item'),
    path('clearcart', clear_cart, name='clear_cart'),
    path('increment_cart_quantity/<int:item_id>/', increment_cart_quantity, name='increment_cart_quantity'),
    path('decrement_cart_quantity/<int:item_id>/', decrement_cart_quantity, name='decrement_cart_quantity'),

    # for checkout page
    path('checkout/', checkoutView, name='checkout'),


]