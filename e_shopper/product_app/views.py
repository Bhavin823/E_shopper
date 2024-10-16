from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from product_app.models import ProductModel,ProductSize
from category_app.models import SubCategoryModel
from django.contrib.auth.decorators import login_required
from category_app.views import Cat_Subcat_Nav_View,cart_total_quantity
from cart_app.models import CartModel,CartItemModel

# Create your views here.

def ProductView(request,subcatslug):
    if subcatslug == 'all':
        products = ProductModel.objects.filter(is_active=True) # Fetch all active products
        subcateheadername = "All Products" # Set subcategory name to "All Products"
        category = None
        product_with_same_category = ProductModel.objects.none()
        
        # print(product_with_same_category)
    
    else:
        subcategoryslug = get_object_or_404(SubCategoryModel, slug=subcatslug) #fetch slug of specified product
        products  = ProductModel.objects.filter(subcategory=subcategoryslug, is_active=True) #fetch those product which subcategort match and active products
        subcateheadername = subcategoryslug.subcategoryName # Get the name of the subcategory
        category = subcategoryslug.category
        
        # recommended products from the same category
        product_with_same_category = ProductModel.objects.filter(category=category).exclude(subcategory=subcategoryslug)
        # print(product_with_same_category)
    
    cat_subcat_for_nav = Cat_Subcat_Nav_View()  # left sidebar 
    
    cart_total_quan = cart_total_quantity(request) # cart total quantity

    if request.user.is_authenticated:
        for product in products:
            product.quantity_in_cart = 0  # Default value if not in cart
            for item in request.user.cartmodel.items.all():
                if item.product == product:
                    product.quantity_in_cart = item.quantity

        for product in product_with_same_category:
            product.quantity_in_cart = 0  # Default value if not in cart
            for item in request.user.cartmodel.items.all():
                if item.product == product:
                    product.quantity_in_cart = item.quantity

    
    
    context = {
        'cat_sub_nav' : cat_subcat_for_nav,
        'subcateheadername':subcateheadername,
        'products' : products,
        'subcatslug':subcatslug,
        'product_with_same_category':product_with_same_category,
        'cart_total_quantity':cart_total_quan,
        'category':category,
    }
    return render(request,'product_app/product.html',context)

def ProductDetailView(request, productslug):
    productdetail = get_object_or_404(ProductModel, slug=productslug, is_active=True)
    product_with_same_subcategory = ProductModel.objects.filter(
        subcategory=productdetail.subcategory, is_active=True
    ).exclude(id=productdetail.id)

    available_sizes = productdetail.sizes.all()
    cat_subcat_for_nav = Cat_Subcat_Nav_View()  # left sidebar
    cart_total_quan = 0
    cart_item = None  # Default value if user is not logged in

    if request.user.is_authenticated:
        try:
            cart_item = CartItemModel.objects.get(user=request.user, product=productdetail)
        except CartItemModel.DoesNotExist:
            cart_item = None

        cart_total_quan = cart_total_quantity(request)  # cart total quantity
        productdetail.quantity_in_cart = 0
        for item in request.user.cartmodel.items.filter(product=productdetail):
            productdetail.quantity_in_cart += item.quantity

        for product in product_with_same_subcategory:
            product.quantity_in_cart = 0  # Default value if not in cart
            for item in request.user.cartmodel.items.filter(product=product):
                product.quantity_in_cart += item.quantity

        # Find the cart item with the specific size
        selected_size_id = request.GET.get('size', '')
        if selected_size_id:
            # If a size is provided, get the corresponding ProductSize object
            selected_size = get_object_or_404(ProductSize, id=selected_size_id)
            try:
                # Try to find the cart item with the specified size
                cart_item = CartItemModel.objects.get(user=request.user, product=productdetail, size=selected_size)
            except CartItemModel.DoesNotExist:
                cart_item = None
        else:
            # If no size is provided, find if any size is in the cart
            for size in available_sizes:
                try:
                    cart_item = CartItemModel.objects.get(user=request.user, product=productdetail, size=size)
                    if cart_item:
                        break
                except CartItemModel.DoesNotExist:
                    continue
    
    context = {
        'cat_sub_nav': cat_subcat_for_nav,
        'productdetail': productdetail,
        'product_with_same_subcategory': product_with_same_subcategory,
        'cart_total_quantity': cart_total_quan,
        'available_sizes': available_sizes,
        'cart_item': cart_item,  # cart_item will be None if the user is not logged in
    }
    return render(request, 'product_app/productdetail.html', context)

def product_list(request):
    query = request.GET.get('q')
    if query:
        # Filter products by category, subcategory, or product name
        products = ProductModel.objects.filter(
            Q(ProductName__icontains=query) |  # Search by product name
            Q(category__categoryName__icontains=query) |  # Search by category name
            Q(subcategory__subcategoryName__icontains=query),  # Search by subcategory name
            is_active=True  # Ensure only active products are shown
        )
    else:
        products = ProductModel.objects.filter(is_active=True)
    
    cat_subcat_for_nav = Cat_Subcat_Nav_View()  # left sidebar 
    
    cart_total_quan = cart_total_quantity(request) # cart total quantity


    context = {
        'products':products,
        'cat_sub_nav' : cat_subcat_for_nav,
        'cart_total_quan':cart_total_quan,
    }    
    return render(request,'product_app/product_list.html',context)
