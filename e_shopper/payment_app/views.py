from django.shortcuts import render,redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,Http404
from order_app.models import OrderModel,OrderItem
from cart_app.models import CartModel,CartItemModel
from django.contrib.auth.decorators import login_required
from .models import RazorpayOrder,RazorpayPayment
from datetime import datetime
import json
from django.urls import reverse

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def order_payment(request,order_id):
    request.session['user_id'] = request.user.id
    order = OrderModel.objects.get(id=order_id)
    

    # Create a Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': int(float(order.total_amount) * 100),  # Razorpay expects amount in paise
        'currency': 'INR',
        'payment_capture': 1,  # Auto-capture payment after order creation
    })

    # Save Razorpay order ID in your OrderModel
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    # print("callbackurl",request.build_absolute_uri(reverse('payment_app:callback')))
    # Render payment template with context
    return render(
        request,
        "payment_app/pyment.html",
        {
            "callback_url": request.build_absolute_uri(reverse('payment_app:callback')),
            "razorpay_key": settings.RAZOR_KEY_ID,
            "order": order,
            'razorpay_order': razorpay_order,
        },
    )

@csrf_exempt
def callback(request):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    def verify_signature(response_data):
        try:
            client.utility.verify_payment_signature(response_data)
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
        
    if request.method == "GET" and request.GET.get('status') == "failure":
        razorpay_order_id = request.GET.get('order_id')
        
        # fetch order detail from razorpay
        order_details = client.order.fetch(razorpay_order_id)
        
        # Save RazorpayOrder details
        razorpay_order, created = RazorpayOrder.objects.update_or_create(
            order_id=order_details['id'],
            defaults={
                'amount': order_details['amount'],
                'currency': order_details['currency'],
                'status': order_details['status'],
                'attempts': order_details['attempts'],
                'created_at': datetime.fromtimestamp(order_details['created_at'])
            }
        )

        # If the order status is 'attempted', fetch and save payment details 
        if order_details['status'] == 'attempted':
            payment_collection  = client.order.payments(order_details['id'])
            # print(payment_collection)
            for payment in payment_collection['items']:
                RazorpayPayment.objects.update_or_create(
                    payment_id = payment['id'],
                    defaults={
                        'order':razorpay_order,
                        'amount': payment['amount'],
                        'status': payment['status'],
                        'method': payment['method'],
                        'created_at': datetime.fromtimestamp(payment['created_at']),
                        'error_reason': payment.get('error_reason', ''),
                        'error_code': payment.get('error_code', '')
                    }
                )

        order = OrderModel.objects.get(razorpay_order_id=razorpay_order_id)
        order.status = "pending"
        order.payment_status = "failed"
        order.save()
        # print("get:",order.status,order.payment_status)
        context={
            "status":order.status,
            "payment_status":order.payment_status
        }
        return render(request,'payment_app/payment_success.html',context)
    
    
    if request.method == "POST":
        user = request.user

        if "razorpay_signature" in request.POST:
            razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            razorpay_signature_id = request.POST.get("razorpay_signature", "")

            # Save RazorpayOrder details
            order_details = client.order.fetch(razorpay_order_id)
            # print("post:",order_details)
            razorpay_order, created = RazorpayOrder.objects.update_or_create(
                order_id=order_details['id'],
                defaults={
                    'amount': order_details['amount'],
                    'currency': order_details['currency'],
                    'status': order_details['status'],
                    'attempts': order_details['attempts'],
                    'created_at': datetime.fromtimestamp(order_details['created_at'])
                }
            )

            # If the order status is 'attempted', fetch payment details
            if order_details['status'] == 'attempted' or order_details['status'] == 'paid':
                payment_collection  = client.order.payments(order_details['id'])
                # print(payment_collection)
                for payment in payment_collection['items']:
                    RazorpayPayment.objects.update_or_create(
                        payment_id = payment['id'],
                        defaults={
                            'order':razorpay_order,
                            'amount': payment['amount'],
                            'status': payment['status'],
                            'method': payment['method'],
                            'created_at': datetime.fromtimestamp(payment['created_at']),
                            'error_reason': payment.get('error_reason', ''),
                            'error_code': payment.get('error_code', '')
                        }
                    )
            order = OrderModel.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature_id
            order.save()

            if verify_signature(request.POST):
                order.status = "pending"
                order.payment_status = "paid"
                order.save()
                cart = CartModel.objects.get(user=order.user)
                cart_items = cart.items.all()
                cart_items.delete()
                # print("signature true:",order.status,order.payment_status)
                context = {
                    "status": order.status,
                    "payment_status":order.payment_status
                }
                return render(request, 'payment_app/payment_success.html', context)
            else:
                order.status = "canceled"
                order.payment_status = "failed"
                order.save()
                # print("signature false:",order.status,order.payment_status)
                context = {
                    "status": order.status,
                    "payment_status":order.payment_status
                }
                return render(request, 'payment_app/payment_success.html', context)
        else:
            razorpay_payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            razorpay_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
            
            # Save RazorpayOrder details
            order_details = client.order.fetch(razorpay_order_id)

            # print("post:",order_details)
            razorpay_order, created = RazorpayOrder.objects.update_or_create(
                order_id=order_details['id'],
                defaults={
                    'amount': order_details['amount'],
                    'currency': order_details['currency'],
                    'status': order_details['status'],
                    'attempts': order_details['attempts'],
                    'created_at': datetime.fromtimestamp(order_details['created_at'])
                }
            )

            # If the order status is 'attempted', fetch payment details
            if order_details['status'] == 'attempted' or order_details['status'] == 'paid':
                payment_collection  = client.order.payments(order_details['id'])
                # print(payment_collection)
                for payment in payment_collection['items']:
                    RazorpayPayment.objects.update_or_create(
                        payment_id = payment['id'],
                        defaults={
                            'order':razorpay_order,
                            'amount': payment['amount'],
                            'status': payment['status'],
                            'method': payment['method'],
                            'created_at': datetime.fromtimestamp(payment['created_at']),
                            'error_reason': payment.get('error_reason', ''),
                            'error_code': payment.get('error_code', '')
                        }
                    )

            order = OrderModel.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.status = "canceled"
            order.payment_status = "failed"
            order.save()
            # print("get error: ",order.status,order.payment_status)
            context={
                "status": order.status,
                "payment_status":order.payment_status
                }
            return render(request, 'payment_app/payment_success.html', context)
    else:
        context = {
            "status": "Invalid request method",
        }
        return render(request, 'payment_app/payment_success.html', context)

@login_required
def payment_success_page(request):
    return render(request,'payment_app/payment_success.html')
