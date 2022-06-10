from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Chef


class ChefUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']



class ChefForm(forms.ModelForm):
    class Meta:
        model=Chef
        fields=['mobile_number','profile_pic','resume']

    

class ChefUserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']


class ChefUpdateForm(forms.ModelForm):
    class Meta:
        model=Chef
        fields=['profile_pic','mobile_number']