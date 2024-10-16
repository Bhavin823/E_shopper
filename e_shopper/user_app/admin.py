# Register your models here.
from django.contrib import admin
from .models import UserProfile,UserAddress

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact','firstname','lastname','gender')

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user','name','contact','pincode','address','city','state','addresstype')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)