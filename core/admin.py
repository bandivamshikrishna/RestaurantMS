from django.contrib import admin
from .models import ReserveTable,ReserveFood


# Register your models here.
@admin.register(ReserveTable)
class ReserveTableAdmin(admin.ModelAdmin):
    list_display=['id','seater','table_pic']

@admin.register(ReserveFood)
class ReserveFoodAdmin(admin.ModelAdmin):
    list_display=['id','name','price','food_type','food_pic']