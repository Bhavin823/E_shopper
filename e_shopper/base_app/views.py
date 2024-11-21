from django.shortcuts import render
from category_app.views import CategoryView,Cat_Subcat_Nav_View
from cart_app.views import cart_total_quantity
from product_app.models import ProductModel
from category_app.models import CategoryModel
from django.templatetags.static import static

# Create your views here.
def baseview(request):
    cart_total_quan = cart_total_quantity(request)
    context = {
        'cart_total_quantity':cart_total_quan,
    }
    return render(request,'base_app/base.html',context)

def homeview(request):
    banner_image_url = request.build_absolute_uri(static('images/shop/eshopper_banner.png'))
    categories = CategoryView()
    # fetch 6 random products for recommended items
    recommended_products = ProductModel.objects.all().filter(is_active=True).order_by('?')[:6].prefetch_related('images')
    for category in categories:
        # custom attribute to hold 3 random products
        category.random_products = category.products.all().order_by('?').filter(is_active=True)[:3].prefetch_related('images')
    cat_subcat_for_nav = Cat_Subcat_Nav_View()
    cart_total_quan = cart_total_quantity(request)
    context = {
        'categories': categories,
        'cat_sub_nav' : cat_subcat_for_nav,
        'cart_total_quantity':cart_total_quan,
        'recommended_products': recommended_products,
        'banner_image_url':banner_image_url,
    }
    return render(request,'base_app/home.html',context)


