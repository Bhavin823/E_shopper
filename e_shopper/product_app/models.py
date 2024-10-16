from django.db import models
from django.utils.text import slugify
from category_app.models import CategoryModel,SubCategoryModel

# Create your models here.


class ProductModel(models.Model):
    ProductName = models.CharField(max_length=100)
    ProductImage = models.ImageField(blank=True,upload_to='product/')
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategoryModel,on_delete=models.CASCADE)
    brandName = models.CharField(max_length=100)
    ProductPrice =models.IntegerField()
    sellerName = models.CharField(max_length=100)
    ProductDetail = models.TextField()
    is_active = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ProductName)  # Generate slug from product name
        super(ProductModel, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self) -> str:
        return self.ProductName

class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        # Add more as needed
    ]

    product = models.ForeignKey(ProductModel, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    additional_price = models.IntegerField(default=0)  

    def __str__(self):
        return f'{self.product.ProductName} - {self.size}'
        
