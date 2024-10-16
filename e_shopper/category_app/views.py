from django.shortcuts import render,get_object_or_404
from category_app.models import *
from cart_app.views import cart_total_quantity

# Create your views here.
# for left navigation category and subcategory 
def Cat_Subcat_Nav_View():
    categories= CategoryModel.objects.all()

    categoryHeader=[]
    for category in categories:
        subcategories=SubCategoryModel.objects.filter(category=category.pk)
        
        subcategoryArray=[]
        for subcategory in subcategories:
            subcategoryDict = {"subId:":subcategory.pk,"subName":subcategory.subcategoryName,"subslug":subcategory.slug}
            subcategoryArray.append(subcategoryDict)
            # print(subcategoryArray)
        
        categoryDict={"cat_Id":category.pk,"catName":category.categoryName,"subcategory":subcategoryArray,"cat_Slug":category.slug}
        
        categoryHeader.append(categoryDict)
    # print("category list:",categoryHeader)

    return categoryHeader

# fech all category
def CategoryView():
    categories = CategoryModel.objects.all()
    
    # print("category from category_app:",)
    return categories

# test subcategorypage
def SubcategoryView(request,catslug):
    categoryslug = get_object_or_404(CategoryModel, slug=catslug)  # fetch category slug  
    subcatedata = SubCategoryModel.objects.filter(category=categoryslug)  # fetch subcategory which match with category
    
    cat_subcat_for_nav = Cat_Subcat_Nav_View() # for leftsidebar

    catheadername = CategoryModel.objects.get(slug=catslug)  # for display categoryname on subcategory page
    
    cart_total_quan = cart_total_quantity(request) # cart total quantity
    
    context = {
        'cat_sub_nav':cat_subcat_for_nav,
        'catheadername':catheadername,
        'subcategories':subcatedata,
        'cart_total_quantity':cart_total_quan,
    }
    return render(request,'category_app/subcategory.html',context)
