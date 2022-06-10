from django.db import models

# Create your models here.
seater_choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(8,8),(10,10),(20,20))
class ReserveTable(models.Model):
    seater=models.IntegerField(choices=seater_choices)
    table_pic=models.ImageField(upload_to='table_pic/',null=True,blank=True)
    

type=(('nonveg','NonVeg'),('veg','Veg'),('soups','Soups'),('drinks','Drinks'))
class ReserveFood(models.Model):
    name=models.CharField(max_length=40)
    price=models.IntegerField()
    food_type=models.CharField(max_length=40,choices=type,null=True)
    food_pic=models.ImageField(upload_to='food_pic/',null=True,blank=True)

    def __str__(self):
        return self.name



class Rating(models.Model):
    rating=models.PositiveIntegerField()
    data=models.TextField()