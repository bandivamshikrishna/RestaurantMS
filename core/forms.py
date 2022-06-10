from django import forms
from .models import Rating, ReserveTable,ReserveFood


class ReserveTableForm(forms.ModelForm):
    class Meta:
        model=ReserveTable
        fields=['seater','table_pic']



class ReserveFoodForm(forms.ModelForm):
    class Meta:
        model=ReserveFood
        fields=['name','price','food_type','food_pic']


class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['data']