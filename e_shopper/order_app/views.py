from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from user_app.models import UserAddress
from cart_app.models import CartModel,CartItemModel
from order_app.models import OrderModel,OrderItem
from payment_app.models import RazorpayPayment,RazorpayOrder
from django.shortcuts import get_object_or_404


# Create your views here.
def create_order(request):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('address_id')
        # print("address id:",address_id)
        total_amount = request.POST.get('totalamount')
        # print(total_amount)
        if total_amount is None:
            messages.error(request, 'Cart Has Not Any Items')
            return redirect('cart_app:checkout')
        payment_type  = request.POST.get('PaymentType')
        # print(payment_type)
        address = UserAddress.objects.get(pk=address_id)
        cart = CartModel.objects.get(user=user)
        cart_items = cart.items.all()
        # print("cart items during cart items: ",cart_items)
        
        order = OrderModel.objects.create(
            user = user,
            shipping_address = address,
            payment_type = payment_type,
            total_amount = total_amount,
        )
        # order.ordered_items.set(cart_items)
        cart_item = CartItemModel.objects.filter(user=user)
        for item in cart_item:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.final_price,
                size = item.size
            )

        if payment_type == 'Cash On Delivary':
            order.status = 'pending'
            order.payment_status = 'pending'
            order.shipping_cost = 100
            order.save()
        elif payment_type == 'Online':
            # return redirect('payment_app:initialize_razorpay', order_id=order.id)
            return redirect('payment_app:payment',order_id=order.id)
            

        cart_items.delete()
        cart_item.delete()

        response_data = {
                'message': 'Order successfully created',
                'selected_address_id': address_id,
                'totalamount':total_amount,
                'payment_type': payment_type,
            }
    print(order.status)
    print(order.payment_status)
    context={
        "status": order.status,
        "payment_status":order.payment_status,
        }
    
    return render(request, 'payment_app/payment_success.html',context)
    # return JsonResponse(response_data)

def order_detail(request,id):
    order = get_object_or_404(OrderModel, id=id)
    order_itemm = OrderItem.objects.filter(order=order)
    total_order_amount = order.total_amount
    shipping_cost = order.shipping_cost
    # print(shipping_cost)
    quantity = 0
    for item in order_itemm:
        # print(item.quantity)
        quantity = quantity+item.quantity


    for item in order_itemm:
        if item.size:
            print(item.size.size)
        else:
            print(item.size)
    
    try:
        # Assuming 'razorpay_order_id' links to 'order_id' in RazorpayOrder
        razorpay_order = RazorpayOrder.objects.get(order_id=order.razorpay_order_id)
        order.razorpay_order = razorpay_order  # Attach RazorpayOrder instance to OrderModel
        
        # Fetch payments related to the RazorpayOrder
        payments = RazorpayPayment.objects.filter(order=razorpay_order)
        order.payment_methods = [payment.method for payment in payments]
        # print(order.payment_methods)
    except RazorpayOrder.DoesNotExist:
        order.razorpay_order = None  # Handle case where no RazorpayOrder exists
    context = {
        'my_order': order,
        'my_order_item_detail' : order_itemm,
        'total_order_amount':total_order_amount,
        'shipping_cost':shipping_cost,
        'no_of_item':quantity,
    }
    return render(request,'order_app/od.html',context)



def invoice(request,id):
    order= OrderModel.objects.get(id=id)
    # print(order)
    order_itemm = OrderItem.objects.filter(order=order)
    # print("order_item: ",order_itemm)
    total_order_amount = order.total_amount
    shipping_cost = order.shipping_cost
    
    total_payment = total_order_amount+shipping_cost

    has_size = any(item.size for item in order_itemm)
    
    context = {
        'my_order': order,
        'my_order_item_detail' : order_itemm,
        'total_order_amount':total_order_amount,
        'shipping_cost':shipping_cost,
        'total_payment':total_payment,
        'has_size':has_size,
    }
    return render(request,'order_app/invoice.html',context)

