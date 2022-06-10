from django.shortcuts import render,HttpResponseRedirect
from .forms import ChefUserForm,ChefForm,ChefUserUpdateForm,ChefUpdateForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Chef
from customer.models import FoodOrder,TableOrder
from django.db.models import Q

# Create your views here.
def chef_sign_up(request):
    if request.method=='POST':
        chef_form=ChefForm(request.POST,request.FILES)
        user_form=ChefUserForm(request.POST)
        position=request.POST.getlist('dropdown[]')
        if chef_form.is_valid() and user_form.is_valid():
            user=user_form.save()
            chef=chef_form.save(commit=False)
            chef.user=user
            chef.position=position
            chef.save()
            chef_group,created=Group.objects.get_or_create(name='CHEF')
            user.groups.add(chef_group)
            return HttpResponseRedirect('/customer/signin/')
    else:
        chef_form=ChefForm()
        user_form=ChefUserForm()
    return render(request,'chef/signup.html',{'chefform':chef_form,'userform':user_form})



def chef_sign_in(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            next=request.POST.get('next')
            request.session['next']=next
            auth_form=AuthenticationForm(request=request,data=request.POST)
            if auth_form.is_valid():
                username=auth_form.cleaned_data.get('username')
                password=auth_form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/afterlogin/')
        else:
            auth_form=AuthenticationForm()
        return render(request,'chef/signin.html',{'authform':auth_form})
    else:
        return HttpResponseRedirect('/chef/foodorders/')


def chef_not_approved(request):
    return render(request,'chef/notapproved.html')


@login_required(login_url='chef-sign-in')
def chef_food_orders(request):
    table_orders=TableOrder.objects.all()
    food_orders=FoodOrder.objects.filter(~Q(table=None))
    return render(request,'chef/foodorders.html',{'foodorders':food_orders})


@login_required(login_url='chef-sign-in')
def chef_food_deliveries(request):
    food_orders=FoodOrder.objects.filter(~(Q(address1=None)))
    return render(request,'chef/fooddeliveries.html',{'foodorders':food_orders})


@login_required(login_url='chef-sign-in')
def chef_profile(request):
    chef=Chef.objects.get(user=request.user)
    user=User.objects.get(id=chef.user_id)
    return render(request,'chef/profile.html',{'chef':chef,'user':user})





@login_required(login_url='chef-sign-in')
def chef_edit_profile(request):
    chef=Chef.objects.get(user=request.user)
    user=User.objects.get(id=chef.user_id)
    if request.method=='POST':
        chef_update_form=ChefUpdateForm(request.POST,request.FILES,instance=chef)
        user_update_form=ChefUserUpdateForm(request.POST,instance=user)
        if chef_update_form.is_valid() and user_update_form.is_valid():
            user=user_update_form.save()
            chef=chef_update_form.save(commit=False)
            chef.user=user
            chef.save()
            return HttpResponseRedirect('/chef/profile/')
    else:
        chef_update_form=ChefUpdateForm(instance=chef)
        user_update_form=ChefUserUpdateForm(instance=user)
    return render(request,'chef/editprofile.html',{'chefupdateform':chef_update_form,'userupdateform':user_update_form})


@login_required(login_url='chef-sign-in')
def chef_change_password(request):
    if request.method=='POST':
        password_form=PasswordChangeForm(user=request.user,data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request,password_form.user)
            return HttpResponseRedirect('/chef/profile/')
    else:
        password_form=PasswordChangeForm(user=request.user)
    return render(request,'chef/changepassword.html',{'passwordform':password_form})


@login_required(login_url='chef-sign-in')
def chef_logout(request):
    logout(request)
    return HttpResponseRedirect('/chef/signin/')