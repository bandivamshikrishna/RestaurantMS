from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from customer.models import FoodOrder,TableOrder
from .forms import ReserveFoodForm, ReserveTableForm,RatingForm
from chef.models import Chef
from django.contrib.auth.models import User
from .models import Rating,ReserveTable

# Create your views here.

def home(request): 
    return render(request,'core/home.html')

def about(request):
    ratings=Rating.objects.all().order_by('-id')[0:3]
    context={
        'rating1':ratings[0],
        'rating2':ratings[1],
        'rating3':ratings[2],
        'rating1_rating':range(ratings[0].rating),
        'rating2_rating':range(ratings[1].rating),
        'rating3_rating':range(ratings[2].rating),
    }
    return render(request,'core/about.html',context=context)


def review(request):
    if request.method=='POST':
        rating=0
        form=RatingForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data.get('data')
            if request.POST.get('rating1'):
                rating=1
            elif request.POST.get('rating2'):
                rating=2
            elif request.POST.get('rating3'):
                rating=3
            elif request.POST.get('rating4'):
                rating=4
            elif request.POST.get('rating5'):
                rating=5
            ratingdata=Rating(rating=rating,data=data)
            ratingdata.save()
            return HttpResponseRedirect('/about/')
    else:
        form=RatingForm()
    return render(request,'core/review.html',{'form':form})


def menu(request):
    return render(request,'core/menu.html')


def table_booking(request):
    tables=ReserveTable.objects.all()
    return render(request,'core/tablebooking.html',{'tables':tables})


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def is_chef(user):
    return user.groups.filter(name='CHEF').exists()


def is_admin(user):
    if user.is_superuser==True:
        return True
    else:
        return False


def afterlogin(request):
    if(is_customer(request.user)):
        if request.session['next']:
            next=request.session['next']
            if next:
                return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/customer/dashboard/')
    elif(is_chef(request.user)):
        approved=Chef.objects.filter(user_id=request.user.id,approved=True)
        if approved:
            if request.session['next']:
                next=request.session['next']
                if next:
                    return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/chef/foodorders/')
        else:
            return HttpResponseRedirect('/chef/chefnotapproved/')
    elif(is_admin(request.user)):
        if request.session['next']:
            next=request.session['next']
            if next:
                return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/admin-food-deliveries/')




def admin_sign_in(request):
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
        auth_form=AuthenticationForm()
        return render(request,'chef/signin.html',{'authform':auth_form})
    else:
        return HttpResponseRedirect('/admin-food-deliveries/')



@login_required(login_url='admin-sign-in')
def admin_add_table(request):
    if request.method=='POST':
        table_form=ReserveTableForm(request.POST,request.FILES)
        if table_form.is_valid():
            table_form.save()
            return HttpResponseRedirect('/admin-add-table/')
    else:
        table_form=ReserveTableForm()
    return render(request,'admin/addtable.html',{'tableform':table_form})


@login_required(login_url='admin-sign-in')
def admin_add_food(request):
    if request.method=='POST':
        food_form=ReserveFoodForm(request.POST,request.FILES)
        if food_form.is_valid():
            food_form.save()
            return HttpResponseRedirect('/admin-add-food/')
    else:
        food_form=ReserveFoodForm()
    return render(request,'admin/addfood.html',{'foodform':food_form})




@login_required(login_url='admin-sign-in')
def admin_table_orders(request):
    table_orders=TableOrder.objects.all()
    return render(request,'admin/tableorders.html',{'tableorders':table_orders})


@login_required(login_url='admin-sign-in')
def admin_food_orders(request):
    food_orders=FoodOrder.objects.filter(~Q(address1=None))
    return render(request,'admin/foodorders.html',{'foodorders':food_orders})



@login_required(login_url='admin-sign-in')
def admin_food_deliveries(request):
    food_orders=FoodOrder.objects.filter(~Q(address1=None))
    return render(request,'admin/fooddeliveries.html',{'foodorders':food_orders})


@login_required(login_url='admin-sign-in')
def admin_approved_chef(request):
    chefs=Chef.objects.filter(approved=True)
    return render(request,'admin/approvedchef.html',{'chefs':chefs})


@login_required(login_url='admin-sign-in')
def admin_approving_chef(request,id):
    chef=Chef.objects.get(id=id)
    chef.approved=True
    chef.save()
    return HttpResponseRedirect('/admin-approved-chef/')

@login_required(login_url='admin-sign-in')
def admin_rejecting_chef(request,id):
    chef=Chef.objects.get(id=id)
    user=User.objects.get(id=chef.user_id)
    chef.delete()
    user.delete()
    return HttpResponseRedirect('/admin-pending-chef/')


@login_required(login_url='admin-sign-in')
def admin_pending_chef(request):
    chefs=Chef.objects.filter(approved=False)
    return render(request,'admin/pendingchef.html',{'chefs':chefs})

@login_required(login_url='admin-sign-in')
def admin_parking_details(request):
    food_orders=FoodOrder.objects.filter(~Q(parking=None))
    return render(request,'admin/parking.html',{'foodorders':food_orders})



@login_required(login_url='admin-sign-in')
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin-signin/')