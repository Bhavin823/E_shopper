from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    GENDER_CHOICE  = (
        ('M','Male'),
        ('F','Female'),
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICE, blank=True)
    
class UserAddress(models.Model):    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    STATE_CHOICE = (
        ('Arunachal Pradesh','Arunachal Pradesh'),
        ('Andman & Nicobar','Andman & Nicobar'),
        ('Assam','Assam'),
        ('Bihar','Bihar'),
        ('Chandigarh','Chandigarh'),
        ('Chattisgadh','Chattisgadh'),
        ('Dadra Nagar','Dadra Nagar'),
        ('Daman & Diu','Daman & Diu'),
        ('Delhi','Delhi'),
        ('Goa','Goa'),
        ('Gujrat','Gujrat'),
        ('Haryana','Haryana'),
        ('Himachal Pradesh','Himachal Pradesh'),
        ('Jammu','Jammu'),
        ('Jarkhand','Jarkhand'),
        ('Karnataka','Karnataka'),
        ('Kerala','Kerala'),
        ('Ladakh','Ladakh'),
        ('Madhya Pradesh','Madhya Pradesh'),
        ('Manipur','Manipur'),
        ('Maharashtra','Maharashtra'),
        ('Meghalaya','Meghalaya'),
        ('Mizoram','Mizoram'),
        ('Nagaland','Nagaland'),
        ('Odhisha','Odhisha'),
        ('Punjab','Punjab'),
        ('Rajasthan','Rajasthan'),
        ('Sikkim','Sikkim'),
        ('Tripura','Tripura'),
        ('Tamil Nadu','Tamil Nadu'),
        ('Telgana','Telgana'),
        ('Utar Prades','Utar Prades'),
        ('Utrakhand','Utrakhand'),
        ('West Benagal','West Benagal'),
    )
    state  = models.CharField(max_length=255,choices=STATE_CHOICE)
    landmark = models.CharField(max_length=100)
    optionalnumber = models.CharField(max_length=10,blank=True)
    ADDRESS_TYPE = (
        ('Home','HOME'),
        ('Work','WORK'),
    )
    addresstype = models.CharField(max_length=10,choices=ADDRESS_TYPE)