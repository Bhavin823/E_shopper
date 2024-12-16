from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from user_app.models import UserProfile,UserAddress
from order_app.models import OrderModel
from payment_app.models import RazorpayOrder,RazorpayPayment
from cart_app.views import cart_total_quantity
from django.contrib import messages

# Create your views here.
# signup page
def signupView(request):  
     # Render the signup.html template
    return render(request,'user_app/signup.html')

# handle signup
def handelSignup(request):
    if request.method == "POST":
         # Get the POST values from the form
        username = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        password1 = request.POST['pass']
        password2 = request.POST['re_pass']
        
        # Check if password1 and password2 match
        if password1 == password2:
            
            # Check if a user with the same email or username already exists
            data = User.objects.filter(Q(email=email) | Q(username=username)) 
            if len(data) <= 0:
                
                # Create a new User instance
                myuser = User.objects.create_user(username, email, password1)
                
                # Create a UserProfile instance and associate it with the user
                user_profile = UserProfile.objects.create(user=myuser, contact=contact)
                
                # Render a success message
                return render(request,'user_app/login.html',{'messagekey':'Registration Successful!'})
            else:
                # Render a message for existing user
                return render(request,'user_app/signup.html',{'messagekey':'User Already Exists'})
        else:
            # Render a message for password mismatch
            return render(request,'user_app/signup.html',{'messagekey':'Password Does Not Match'})
    else:
        # Return a 404 response for non-POST requests
        return HttpResponse('404 - Not Found')

# login page
def loginView(request):
    # fetch detail from post page for return after login
    # retpath = request.GET.get('retpath', '')
    # subcatslug = request.GET.get('subcatslug', '')
    # productslug = request.GET.get('productslug', '')
    
    next = request.GET.get('next','')
    
    # print(retpath)
    # print(subcatslug)
    # print(productslug)
    context={
        # 'retpath':retpath,
        # 'subcateslug':subcatslug,
        # 'productslug':productslug,
        'next':next,
    }
    return render(request,'user_app/login.html',context)

# login handle
def handleLogin(request):
    if request.method == "POST":
        # retrive from login form
        retpath = request.POST.get('retpath', '')
        subcatslug = request.POST.get('subcatslug', '')
        productslug = request.POST.get('productslug', '')

        # print("repath:",retpath)
        # print("subcatslug:",subcatslug)
        # print('productslug',productslug)

        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            # If the user is authenticated, log them in and redirect to the home page
            login(request,user)
            print('login successfully')
            # check in url and then redirect to return page
            next_url = request.POST.get('next','')
            print("next_url:",next_url)
            messages.success(request, f"Welcome {user.username}!")
            if retpath == "prolog":
                return redirect('product_app:products',subcatslug=subcatslug)
            elif retpath == 'prodet':
                return redirect('product_app:productdetail',productslug=productslug)
            elif retpath == 'checkout':
                return redirect('cart_app:checkout')
            elif next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            # If authentication fails, render the login page with an error message
            return render(request,'user_app/login.html', {'messagekey':" Inavalid Credentials !"})
    # If the request method is not POST, return a 404 response
    return HttpResponse('404 - Not Found')

# logout handle
def logouthandle(request):
    logout(request)
    print("logout")
    return redirect('home')


# profile page view
@login_required(login_url='user_app:login')
def profileView(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_addresses = UserAddress.objects.filter(user=request.user)
    my_order = OrderModel.objects.filter(user=request.user).order_by('-id')

    cart_total_quan = cart_total_quantity(request)
    
    # Fetching related RazorpayOrder and RazorpayPayment for each OrderModel
    for order in my_order:
        try:
            # Assuming 'razorpay_order_id' links to 'order_id' in RazorpayOrder
            razorpay_order = RazorpayOrder.objects.get(order_id=order.razorpay_order_id)
            order.razorpay_order = razorpay_order  # Attach RazorpayOrder instance to OrderModel
            
            # Fetch payments related to the RazorpayOrder
            payments = RazorpayPayment.objects.filter(order=razorpay_order)
            order.payment_methods = [payment.method for payment in payments]
            
        except RazorpayOrder.DoesNotExist:
            order.razorpay_order = None  # Handle case where no RazorpayOrder exists

    if request.method == 'POST':
        user_profile.firstname = request.POST.get('firstname')
        user_profile.lastname = request.POST.get('lastname')
        user_profile.contact = request.POST.get('contact')
        user_profile.gender = request.POST.get('gender')
        user_profile.save()
    
    context = {
        'user_profile': user_profile,
        'user_addresses': user_addresses,
        'my_order' : my_order,
        'cart_total_quantity':cart_total_quan,
    }
    return render(request,'user_app/profile.html',context)

@login_required
# update profile personal detail
def update_personal_info(request):
    user_profile =  UserProfile.objects.get(user=request.user) 

    # Update the user's first name, last name, and gender
    if request.method == 'POST':
        user_profile.firstname = request.POST.get('firstname')
        print("update",user_profile.firstname)
        user_profile.lastname = request.POST.get('lastname')
        print("update",user_profile.firstname)
        user_profile.gender = request.POST.get('gender')
        print("update",user_profile.gender)
        
        # Save the updated profile
        user_profile.save()
    return redirect('user_app:profile')

# update profile email 
@login_required
def update_email(request):

    # Update the user's email
    if request.method == 'POST':
        new_email = request.POST.get('email')
        print("new_email: ",new_email)
        user = request.user
        user.email = new_email
        print("database email:",user.email)
        # Save the updated email
        user.save()
    
    return redirect('user_app:profile')

# update profile contact
@login_required
def update_contact(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Update the user's contact
    if request.method == 'POST':
        user_profile.contact = request.POST.get('mobileNumber')
        print("update contact: ",user_profile.contact)

        # Save the user contact
        user_profile.save()
    
    return redirect('user_app:profile')

# add address to user profile
@login_required
def add_address(request):
    retpath = request.GET.get('retpath', '')
    if request.method == 'POST':
        name = request.POST.get('name')
        # print(name)
        contact = request.POST.get('mobile')
        # print(contact)
        pincode = request.POST.get('pincode')
        # print(pincode)
        locality = request.POST.get('locality')
        # print(locality)
        address = request.POST.get('address')
        # print(address)
        city = request.POST.get('city')
        # print(city)
        state = request.POST.get('state')
        # print(state)
        landmark = request.POST.get('landmark')
        # print(landmark)
        optionalnumber = request.POST.get('optionalNumber')
        # print(optionalnumber)
        addresstype = request.POST.get('addressType')
        # print(addresstype)

        address = UserAddress(
            user = request.user,
            name = name,
            contact = contact,
            pincode = pincode,
            locality = locality,
            address = address,
            city = city,
            state = state,
            landmark = landmark,
            optionalnumber = optionalnumber,
            addresstype = addresstype
        )
        address.save()
        
    if retpath == "checkout":
            return redirect('cart_app:checkout')

    return redirect('user_app:profile')

# edit user profile particular existed addresses
@login_required
def edit_address(request,address_id):
    retpath = request.GET.get('retpath', '')
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    if request.method == 'POST':

        address.name = request.POST.get('name')  # Use request.POST.get() with a default value
        address.contact = request.POST.get('mobile')
        address.pincode = request.POST.get('pincode')
        address.locality = request.POST.get('locality')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.landmark = request.POST.get('landmark')
        address.optionalnumber = request.POST.get('optionalNumber')
        address.addresstype = request.POST.get('addressType')

        address.save()

        if retpath == "checkout":
            return redirect('cart_app:checkout')

        return redirect('user_app:profile')
    
# delete user profile particular address
@login_required
def delete_address(request,address_id):
    retpath = request.GET.get('retpath', '')
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    
    address.delete()

    if retpath == "checkout":
        return redirect('cart_app:checkout')

    return redirect('user_app:profile')