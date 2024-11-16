from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import ProductModel,ProductSize
from cart_app.models import CartItemModel,CartModel
from user_app.models import UserProfile ,UserAddress
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

# total cart quantity
def cart_total_quantity(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If the user is not logged in, set total quantity to 0
        return 0
    try:
        cart = CartModel.objects.get(user=request.user)
        quantity = 0
        for item in cart.items.all():
            # print(item.quantity)
            quantity = quantity+item.quantity
        # print(quantity)
        return quantity
    except ObjectDoesNotExist:
        quantity = 0
        return quantity

# this function work for specified subcategory product page,all product page,productdetail page
@login_required
def add_to_cart(request, productslug):
    user = request.user
    product = get_object_or_404(ProductModel, slug=productslug)

    # Get the size from the request if available
    size_id = request.GET.get('size', None)
    # product_final_price = request.GET.get('price',None)
    size = None

    if size_id:
        print(size_id)
        # print(product_final_price)
        size = get_object_or_404(ProductSize, id=size_id)

    if size and size.additional_price:
        final_price = product.ProductPrice + size.additional_price
    else:
        final_price = product.ProductPrice

    # Find the user's cart or create a new one
    cart, created = CartModel.objects.get_or_create(user=user)

    # Handle cart item with specific product and size
    cart_item, created = CartItemModel.objects.get_or_create(
        user=user,
        product=product,
        size=size,  # Ensure size is part of the unique combination
        final_price = final_price, # price of selected size
    )
    
    if not created:
        # If the item already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Add the cart item to the user's cart if it's not already added
    if cart_item not in cart.items.all():
        cart.items.add(cart_item)

    subcatslug = request.GET.get('subcatslug', '')
    # print(subcatslug)
    if subcatslug == "all":
        return redirect('product_app:products', subcatslug=subcatslug)
    elif subcatslug == "productdetail":
        return redirect('product_app:productdetail', productslug=productslug)
    else:
        return redirect('product_app:products', subcatslug=subcatslug)

# show cart view with image,name,quantity ,subtotal
@login_required(login_url='user_app:login')
def cartView(request):
    user = request.user

    try:
        cart = CartModel.objects.get(user=user)
    except CartModel.DoesNotExist:
        cart = CartModel.objects.create(user=user)
    

    
    cart_item = cart.items.all()
    # print(cart_item)

    cart_total = sum(item.subtotal() for item in cart_item)

    cart_total_quan = cart_total_quantity(request) # cart total quantity
    # print(total_price)

    has_size = any(item.size for item in cart_item)
    

    context = {
        'cart_items':cart_item,
        'cart': cart,
        'cart_total':cart_total,
        'cart_total_quantity':cart_total_quan,
        'has_size': has_size,
    }

    return render(request,'cart_app/cart.html',context)

# delete specified cart item
def delete_cart_item(request, item_id):
    retpath = request.GET.get('retpath', '')
    try:
        cart_item = CartItemModel.objects.get(id=item_id)
        cart_item.delete()
    except CartItemModel.DoesNotExist:
        # Handle the case where the item doesn't exist
        pass
    if retpath == "checkout":
        return redirect('cart_app:checkout')
    return redirect('cart_app:cart')

# delte whole cart 
def clear_cart(request):
    retpath = request.GET.get('retpath', '')
    # Delete all cart items for the current user
    CartItemModel.objects.filter(user=request.user).delete()
    if retpath == "checkout":
        return redirect('cart_app:checkout')
    # Redirect back to the cart
    return redirect('cart_app:cart')

# increment item quantity
@login_required
def increment_cart_quantity(request,item_id):
    retpath = request.GET.get('retpath', '')
    try:
        cart_item = CartItemModel.objects.get(id=item_id,user=request.user)
        cart_item.quantity +=1
        cart_item.save()
    except CartItemModel.DoesNotExist:
        pass

    if retpath == "checkout":
        return redirect('cart_app:checkout')
    return redirect('cart_app:cart')

# decrement item quantity
@login_required
def decrement_cart_quantity(request, item_id):
    retpath = request.GET.get('retpath', '')
    try:
        cart_item = CartItemModel.objects.get(id=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    except CartItemModel.DoesNotExist:
        pass

    if retpath == "checkout":
        return redirect('cart_app:checkout')
    return redirect('cart_app:cart')

# checkout view
@login_required(login_url='user_app:login')
def checkoutView(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_addresses = UserAddress.objects.filter(user=user)
    cart = CartModel.objects.get(user=user)
    cart_item = cart.items.all()
    cart_total = sum(item.subtotal() for item in cart_item)
    # print(cart_total)
    shipping_cost = 100
    # retpath = request.POST.get('retpath', '')
    # selected_address_id = request.POST.get('selected_address')
    selected_address_id = request.GET.get('selected_address')
    # print("selected_address_id: ",selected_address_id)
    has_size = any(item.size for item in cart_item)
    cart_total_quan = cart_total_quantity(request) # cart total quantity

    context = {
        'cart_items':cart_item,
        'cart': cart,
        'cart_total':cart_total,
        'shipping_cost':shipping_cost,
        'user_profile':user_profile,
        'user_addresses': user_addresses,
        'selected_address_id':selected_address_id,
        'cart_total_quantity':cart_total_quan,
        'has_size':has_size,
    }
    
    return render(request, 'cart_app/checkout.html', context)



