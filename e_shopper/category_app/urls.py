from django.contrib import admin
from django.urls import path
from base_app import views
from category_app.views import *

app_name = 'category_app'

urlpatterns = [
    path('subcat/<slug:catslug>', SubcategoryView, name='subcat'),
    # ... other category app URL patterns ...
]