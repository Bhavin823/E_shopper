from django.db import models
from django.utils.text import slugify

# Create your models here.

class CategoryModel(models.Model):
    categoryName = models.CharField(max_length=100,unique=True)
    categoryImage = models.ImageField(upload_to='category/',blank=True,)
    slug = models.SlugField(unique=True, max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.categoryName)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.categoryName

class SubCategoryModel(models.Model):
    subcategoryName= models.CharField(max_length=100)
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    subcategoryImage = models.ImageField(upload_to='subcategory/',blank=True,)

    slug = models.SlugField(unique=True, max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            category_slug = slugify(self.category.categoryName)
            subcategory_slug = slugify(self.subcategoryName)
            combined_slug = f"{category_slug}-{subcategory_slug}"
            
            counter = 1
            while SubCategoryModel.objects.filter(slug=combined_slug).exclude(id=self.id).exists():
                combined_slug = f"{category_slug}-{subcategory_slug}-{counter}"
                counter += 1
            
            self.slug = combined_slug

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.subcategoryName
