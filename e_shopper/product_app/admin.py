from django.contrib import admin
from product_app.models import ProductModel,ProductSize

# Register your models here.
class ProductSizeInline(admin.TabularInline):
    model  = ProductSize
    extra = 1
    fields = ['size', 'additional_price'] 
    
@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['ProductName','ProductImage','category','subcategory','ProductPrice','is_active']
    inlines = [ProductSizeInline]
