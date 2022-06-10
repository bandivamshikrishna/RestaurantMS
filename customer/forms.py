from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget
from core.models import ReserveFood, ReserveTable
from .models import Customer, FoodOrder,TableOrder,Parking
import datetime


class CustomerUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']


class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['mobile_number','profile_pic']


class TableOrderForm(forms.ModelForm):
    class Meta:
        model=TableOrder
        fields=['table','date','time','seater']
        widgets={
            'date':AdminDateWidget(),
            'time':AdminTimeWidget(),
        }

    def clean(self):
        cleaned_data=super().clean()
        table=self.cleaned_data.get('table')
        date=self.cleaned_data.get('date')
        time=self.cleaned_data.get('time')
        actual_time=datetime.datetime.now().time()
        actual_date=datetime.date.today()
        if date<actual_date:
            raise forms.ValidationError("Can't book a table")
        if time.hour>21:
            raise forms.ValidationError('Sorry its closing time.')
        table_ordered=TableOrder.objects.filter(table=table,date=date).exists()
        if table_ordered:
            table_orders=TableOrder.objects.filter(table=table,date=date)
            for tablee in table_orders:
                if time.hour<actual_time.hour:
                    raise forms.ValidationError("Can't book a table ")
                if time>tablee.pre_time and time>tablee.time and time<tablee.out_time:
                    raise forms.ValidationError('Table Already Booked At this Time')
            
        
        
       
class ReserveFoodOrderForm(forms.ModelForm):
    class Meta:
        model=ReserveFood
        fields=['food_type']


class FoodAddressForm(forms.ModelForm):
    class Meta:
        model=FoodOrder
        fields=['address1','address2','city','state','pincode']


class FoodEditForm(forms.ModelForm):
    class Meta:
        model=FoodOrder
        fields=['food','food_quantity']

        
class ParkingForm(forms.ModelForm):
    class Meta:
        model=Parking
        fields=['vehicle_number']

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['mobile_number','profile_pic']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']


class FoodDeliveryEditForm(forms.ModelForm):
    class Meta:
        model=FoodOrder
        fields=['food','food_quantity','address1','address2','city','state','pincode']