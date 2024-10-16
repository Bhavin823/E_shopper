from django.contrib import admin
from django.urls import path
from user_app.views import *

app_name = 'user_app'

urlpatterns = [
    
    # signup handle
    path('signup/', signupView, name='signup'),
    path('signuphandle', handelSignup, name='signuphandle'),

    # login handle
    path('login/', loginView, name='login'),
    path('loginhandle', handleLogin, name='loginhandle'),

    # logout handle
    path('logouthandle',logouthandle, name='logouthandle'),

    # show profile 
    path('profile',profileView,name='profile'),

    # update_profile_info
    path('update_personal_info/', update_personal_info, name='update_personal_info'),

    # update email
    path('update_email/', update_email,name='update_email'),

    # update contact
    path('update_contact/', update_contact, name='update_contact'),

    # add new address
    path('add_address/', add_address, name='add_address'),

    # edit address
    path('edit_address/<int:address_id>/', edit_address, name='edit_address'),

    # delete address
    path('delete_address/<int:address_id>/', delete_address,name='delete_address'),

]