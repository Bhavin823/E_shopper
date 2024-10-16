from django.shortcuts import render
from category_app.views import CategoryView,Cat_Subcat_Nav_View
from cart_app.views import cart_total_quantity
from product_app.models import ProductModel

# Create your views here.
def baseview(request):
    cart_total_quan = cart_total_quantity(request)
    context = {
        'cart_total_quantity':cart_total_quan,
    }
    return render(request,'base_app/base.html',context)

def homeview(request):
    categories = CategoryView()
    cat_subcat_for_nav = Cat_Subcat_Nav_View()
    # print("categories",categories)
    cart_total_quan = cart_total_quantity(request)
    context = {
        'categories': categories,
        'cat_sub_nav' : cat_subcat_for_nav,
        'cart_total_quantity':cart_total_quan,
    }
    return render(request,'base_app/home.html',context)


