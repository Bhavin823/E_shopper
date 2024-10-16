from django.contrib import admin
from django.urls import path
from product_app.views import ProductView,ProductDetailView,product_list

app_name = 'product_app'

urlpatterns = [
    path('products/<slug:subcatslug>', ProductView, name='products'),
    path('productdetail/<slug:productslug>',ProductDetailView, name = 'productdetail'),
    path('product_list',product_list,name='product_list'),
    # ... other product app URL patterns ...

]