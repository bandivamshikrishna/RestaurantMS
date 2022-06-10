from django.contrib import admin

import customer
from .models import TableOrder,Customer,FoodOrder,Parking


# Register your models here.
@admin.register(TableOrder)
class TableOrderAdmin(admin.ModelAdmin):
    list_display=['id','customer','table','date','time']



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','mobile_number','profile_pic'] 


@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display=['id','customer','table','food','checked','food_quantity','total_price','address1','address2','city','state','pincode','parking']

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display=['customer','vehicle_type','vehicle_number','block','price']