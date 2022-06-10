from django.db import models
from django.contrib.auth.models import User
from core.models import ReserveTable,ReserveFood

# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.PositiveIntegerField()
    profile_pic=models.ImageField(upload_to='customer/profile_pic/')

seater_choices=((2,2),(3,3),(4,4),(5,5),(6,6),(8,8),(10,10),(20,20))
class TableOrder(models.Model):
    table=models.ForeignKey(ReserveTable,on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    seater=models.IntegerField(choices=seater_choices,null=True)
    date=models.DateField(null=True)
    pre_time=models.TimeField(null=True)
    time=models.TimeField(null=True)
    out_time=models.TimeField(null=True)


class Parking(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    vehicle_type=models.CharField(max_length=100)
    vehicle_number=models.CharField(max_length=100)
    block=models.PositiveIntegerField(null=True)
    price=models.PositiveIntegerField(null=True)


type=(('nonveg','NonVeg'),('veg','Veg'),('soups','Soups'),('drinks','Drinks'))
quantity=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(10,10),(20,20))
class FoodOrder(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    food=models.ForeignKey(ReserveFood,on_delete=models.CASCADE,null=True)
    table=models.ForeignKey(TableOrder,on_delete=models.CASCADE,null=True,blank=True)
    checked=models.BooleanField(blank=True,null=True)
    food_quantity=models.IntegerField(choices=quantity,null=True,blank=True)
    total_price=models.IntegerField(null=True,blank=True)

    parking=models.ForeignKey(Parking,on_delete=models.CASCADE,null=True,blank=True)

    address1=models.CharField(max_length=400,blank=True)
    address2=models.CharField(max_length=400,blank=True)
    city=models.CharField(max_length=400,blank=True)
    state=models.CharField(max_length=200,blank=True)
    pincode=models.PositiveIntegerField(null=True,blank=True)


    def __str__(self):
        return self.food.name

