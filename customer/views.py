from django.shortcuts import render,HttpResponseRedirect
from .forms import *
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Customer, FoodOrder,TableOrder,Parking
from core.models import ReserveFood, ReserveTable
from django.core.mail import send_mail
from django.conf import settings
import random
from django.db.models import Q
import datetime




# Create your views here.
def customer_sign_up(request):
    if request.method=='POST':
        customer_form=CustomerForm(request.POST,request.FILES)
        user_form=CustomerUserForm(request.POST)
        if customer_form.is_valid() and user_form.is_valid():
            email=user_form.cleaned_data.get('email')
            username=user_form.cleaned_data.get('username')
            user=user_form.save()
            customer=customer_form.save(commit=False)
            customer.user=user
            customer.save()
            customer_group,created=Group.objects.get_or_create(name='CUSTOMER')
            user.groups.add(customer_group)
            subject='Welcome to Restaurant'
            message='Mr.'+username +'''\n
            Welcome to our Restaturant 
            You have created successfully our account for our Restaurant
            Now u can enjoy all features of our restaturant which is provided by us you can order the food Online, 
            Reserve the table along the food in particular time and with selected guest and also here we are 
            providing the booking to park the vehicle.'''
            send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
            return HttpResponseRedirect('/customer/signin/')
    else:
        customer_form=CustomerForm()
        user_form=CustomerUserForm()
    return render(request,'customer/signup.html',{'customerform':customer_form,'userform':user_form})



def customer_sign_in(request):
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
        return render(request,'customer/signin.html',{'authform':auth_form})
    else:
        return HttpResponseRedirect('/customer/dashboard/')


@login_required(login_url='customer-sign-in',redirect_field_name='next') 
def customer_dashboard(request):
    return render(request,'customer/dashboard.html')


@login_required(login_url='customer-sign-in')
def customer_profile(request):
    customer=Customer.objects.get(user=request.user)
    user=User.objects.get(id=customer.user_id)
    return render(request,'customer/profile.html',{'customer':customer,'user':user})

food_len=0
@login_required(login_url='customer-sign-in')
def customer_food_delivery(request):
    customer=Customer.objects.get(user=request.user)
    food_list=[]
    food_quantity_list=[]
    food_total_price=0
    food_address1=None
    food_address2=None
    reserve_food=ReserveFood.objects.all()
    food_address_form=FoodAddressForm()
    reserve_food_form=ReserveFoodOrderForm()
    if request.method=='POST':
        if request.POST.get('food_type'):
            reserve_food_form=ReserveFoodOrderForm(request.POST)
            if reserve_food_form.is_valid():
                food_type=reserve_food_form.cleaned_data.get('food_type')
                reserve_food=ReserveFood.objects.filter(food_type=food_type)
        else:
            checked_box=request.POST.getlist('checks[]')
            global food_len
            food_len=len(checked_box)
            food_quantity=request.POST.getlist('food_quantity[]')
            number_food_quantity=list()
            for x in food_quantity:
                if x!='':
                    number_food_quantity.append(x)
            number_food_quantity=[int(x) for x in number_food_quantity]
            food_address_form=FoodAddressForm(request.POST)
            if food_address_form.is_valid():
                addr1=food_address_form.cleaned_data.get('address1')
                addr2=food_address_form.cleaned_data.get('address2')
                cityy=food_address_form.cleaned_data.get('city')
                statee=food_address_form.cleaned_data.get('state')
                pin=food_address_form.cleaned_data.get('pincode')
                for x in range(len(checked_box)):
                    food=ReserveFood.objects.get(name=checked_box[x])
                    food_list.append(food.name)
                    checked=True
                    food_quantity=number_food_quantity[x]
                    food_quantity_list.append(food_quantity)
                    total_price=food.price*food_quantity
                    food_total_price=food_total_price+total_price
                    address1=addr1
                    food_address1=address1
                    address2=addr2
                    food_address2=address2
                    city=cityy
                    state=statee
                    pincode=pin
                    food_order=FoodOrder(customer=customer,food=food,checked=checked,food_quantity=food_quantity,total_price=total_price,address1=address1,address2=address2,city=city,state=state,pincode=pincode)
                    food_order.save()
                subject='Welcome to Restaurant'
                message='''
                Dear Mr.'''+request.user.username+'''\n
                Your food is succesfully ordered with food items'''+'''
                '''+str(food_list)+''' with quantity '''+str(food_quantity_list)+''' of total price '''+str(food_total_price)+'''
                we will deliver the food to your location '''+food_address1+''' '''+food_address2+''' in time 
                Enjoy our delicious food .
                '''
                send_mail(subject,message,settings.EMAIL_HOST_USER,[request.user.email])
                return HttpResponseRedirect('/customer/payment/')
    else:
        reserve_food_form=ReserveFoodOrderForm()
        food_address_form=FoodAddressForm()
    return render(request,'customer/fooddelivery.html',{'food':reserve_food,'reservefoodform':reserve_food_form,'foodaddressform':food_address_form})



@login_required(login_url='customer-sign-in')
def customer_food_delivery_edit(request,id):
    food_order=FoodOrder.objects.get(id=id)
    reserve_food=ReserveFood.objects.get(name=food_order)
    if request.method=='POST':
        food_form=FoodDeliveryEditForm(request.POST,instance=food_order)
        if food_form.is_valid():
            food_form.save()
            return HttpResponseRedirect('/customer/tableacknowledgement/')
    else:
        food_form=FoodDeliveryEditForm(instance=food_order)
    return render(request,'customer/fooddeliveryedit.html',{'foodform':food_form})



@login_required(login_url='customer-sign-in')
def customer_food_delivery_delete(request,id):
    food_order=FoodOrder.objects.get(id=id).delete()
    return HttpResponseRedirect('/customer/tableacknowledgement/')

def table_delete_automatic():
    tables=TableOrder.objects.all()
    date=datetime.date.today()
    time=datetime.datetime.now().time()
    for table in tables:
        if date>table.date:
            table.delete()
        elif date==table.date:
            if time>table.out_time:
                table.delete()


@login_required(login_url='customer-sign-in')
def customer_reserve_table(request):
    table_delete_automatic()
    tables=ReserveTable.objects.all()
    return render(request,'customer/reservetable.html',{'tables':tables})


@login_required(login_url='customer-sign-in')
def customer_table_order(request,id):
    table=ReserveTable.objects.get(id=id)
    customer=Customer.objects.get(user=request.user)
    initial_data={
        'table':table,
        'seater':table.seater,
        }
    if request.method=='POST':
        table_order_form=TableOrderForm(request.POST,initial=initial_data)
        if table_order_form.is_valid():
            table_order=TableOrder()
            date=table_order_form.cleaned_data.get('date')
            time=table_order_form.cleaned_data.get('time')
            table_order.table=table
            table_order.customer=customer
            table_order.seater=table.seater
            table_order.date=date
            table_order.time=time
            out_time=time.replace(hour=time.hour+2)
            pre_time=time.replace(hour=time.hour-2)
            table_order.out_time=out_time
            table_order.pre_time=pre_time
            table_order.save()
            return HttpResponseRedirect('/customer/menuyesorno/')
    else:
        table_order_form=TableOrderForm(initial=initial_data) 
    return render(request,'customer/tableorder.html',{'table':table,'tableorderform':table_order_form})


@login_required(login_url='customer-sign-in')
def customer_menu_yes_or_no(request):
    customer=Customer.objects.get(user=request.user)
    table_order=TableOrder.objects.filter(customer=customer).last()
    table_number=table_order.table.id
    return render(request,'customer/menuyes_or_no.html',{'tablenumber':table_number})


@login_required(login_url='customer-sign-in')
def table_booked_mail(request):
    customer=Customer.objects.get(user=request.user)
    last_table_order=TableOrder.objects.filter(customer=customer).last()
    subject='Welcome to Restaurant'
    message='''
    Dear Mr.'''+request.user.username+'''\n
    Your Table is succesfully Booked with '''+'''
    Table No: '''+str(last_table_order.table.id)+''' of '''+str(last_table_order.table.seater)+''' seater
    on '''+str(last_table_order.date)+''' at '''+str(last_table_order.time)+''' time.
    Enjoy our delicious food .
    '''
    print(message)
    send_mail(subject,message,settings.EMAIL_HOST_USER,[request.user.email],fail_silently=True)
    return HttpResponseRedirect('/customer/tableacknowledgement/')


@login_required(login_url='customer-sign-in')
def customer_table_acknowledgement(request):
    table_delete_automatic()
    customer=Customer.objects.get(user=request.user)
    table_order=TableOrder.objects.filter(customer=customer).last()
    table_orders=TableOrder.objects.filter(customer=customer)
    food_orders=FoodOrder.objects.filter(~Q(address1=None)) 
    total_price=0
    for x in food_orders:
        if x.address1:
            total_price=total_price+x.total_price
    return render(request,'customer/tableacknowledgement.html',{'tableorders':table_orders,'foodorders':food_orders,'price':total_price})



@login_required(login_url='customer-sign-in')
def customer_table_edit(request,id):
    table=TableOrder.objects.get(id=id)
    if request.method=='POST':
        table_order=TableOrderForm(request.POST,instance=table)
        if table_order.is_valid():
            customer=Customer.objects.get(user=request.user)
            seater=table_order.cleaned_data.get('seater')
            date=table_order.cleaned_data.get('date')
            time=table_order.cleaned_data.get('time')
            old_table=table_order.cleaned_data.get('table')
            new_table=ReserveTable.objects.get(seater=seater)
            seater=new_table.seater
            out_time=time.replace(hour=time.hour+2)
            table_order_obj=TableOrder(id=id,table=new_table,customer=customer,seater=seater,date=date,time=time,out_time=out_time)
            table_order_obj.save()
            return HttpResponseRedirect('/customer/tableacknowledgement/')

    else:
        table_order=TableOrderForm(instance=table)
    return render(request,'customer/tableedit.html',{'tableorder':table_order})



@login_required(login_url='customer-sign-in')
def customer_table_cancel(request,id):
    table_order=TableOrder.objects.get(id=id).delete()
    return HttpResponseRedirect('/customer/tableacknowledgement/')



@login_required(login_url='customer-sign-in')
def customer_reserve_food(request):
    reserve_food=ReserveFood.objects.all()
    reserve_food_form=ReserveFoodOrderForm()
    if request.method=='POST':
        if request.POST.get('food_type'):
            reserve_food_form=ReserveFoodOrderForm(request.POST)
            if reserve_food_form.is_valid():
                food_type=reserve_food_form.cleaned_data.get('food_type')
                reserve_food=ReserveFood.objects.filter(food_type=food_type)
        else:
            checked_box=request.POST.getlist('checks[]')
            food_quantity=request.POST.getlist('food_quantity[]')
            number_food_quantity=list()
            for x in food_quantity:
                if x!='':
                    number_food_quantity.append(x)
            number_food_quantity=[int(x) for x in number_food_quantity]
            for x in range(len(checked_box)):
                customer=Customer.objects.get(user=request.user)
                food=ReserveFood.objects.get(name=checked_box[x])
                table=TableOrder.objects.filter(customer=customer).last()
                checked=True
                food_quantity=number_food_quantity[x]
                total_price=food.price*food_quantity
                food_order=FoodOrder(customer=customer,food=food,table=table,checked=checked,food_quantity=food_quantity,total_price=total_price)
                food_order.save()
            return HttpResponseRedirect('/customer/parkingyesorno/')        
    else:
        reserve_food_form=ReserveFoodOrderForm()
    return render(request,'customer/reservefood.html',{'food':reserve_food,'reservefoodform':reserve_food_form}) 


@login_required(login_url='customer-sign-in')
def customer_food_acknowledgement(request,id):
    table=TableOrder.objects.get(id=id)
    customer=Customer.objects.get(user=request.user)
    food_orders=FoodOrder.objects.filter(customer=customer).filter(table=table)
    total_price=0
    for food in food_orders:
        total_price=total_price+food.total_price
    return render(request,'customer/foodacknowledgement.html',{'foodorders':food_orders,'total_price':total_price})



@login_required(login_url='customer-sign-in')
def customer_food_edit(request,id):
    food=FoodOrder.objects.get(id=id)
    reserve_food=ReserveFood.objects.get(name=food)
    if request.method=='POST':
        food_form=FoodEditForm(request.POST,instance=food)
        if food_form.is_valid():
            food_quantity=food_form.cleaned_data.get('food_quantity')
            food.total_price=reserve_food.price*food_quantity
            food_form.save()
            return HttpResponseRedirect('/customer/tableacknowledgement/')
    else:
        food_form=FoodEditForm(instance=food)
    return render(request,'customer/foodedit.html',{'foodform':food_form})



@login_required(login_url='customer-sign-in')
def customer_food_cancel(request,id):
    food_order=FoodOrder.objects.get(id=id).delete()
    return HttpResponseRedirect('/customer/tableacknowledgement/')



@login_required(login_url='customer-sign-in')
def customer_parking_yes_or_no(request):
    customer=Customer.objects.get(user=request.user)
    table=TableOrder.objects.filter(customer=customer).last()
    food_order=FoodOrder.objects.filter(customer=customer).filter(table=table)
    food_list=[food.food.name for food in food_order]
    food_quantity=[food.food_quantity for food in food_order]
    return render(request,'customer/parkingyesorno.html',{'table':table,'foodorder':food_order})



@login_required(login_url='customer-sign-in')
def table_food_booked_mail(request):
    customer=Customer.objects.get(user=request.user)
    table=TableOrder.objects.filter(customer=customer).last()
    food_order=FoodOrder.objects.filter(customer=customer).filter(table=table)
    food_list=[food.food.name for food in food_order]
    food_quantity=[food.food_quantity for food in food_order]
    subject='Welcome to Restaurant'
    message='''
    Dear Mr.'''+request.user.username+'''\n
    Your Table is succesfully Booked with '''+'''
    Table No: '''+str(table.table_id)+''' of '''+str(table.table.seater)+''' seater
    on '''+str(table.date)+''' at '''+str(table.time)+''' time.
    with Food Items
    '''+str(food_list)+''' of quantity '''+str(food_quantity)+''' 
    Enjoy our delicious food .
    '''
    print(message)
    send_mail(subject,message,settings.EMAIL_HOST_USER,[request.user.email],fail_silently=True)
    return HttpResponseRedirect('/customer/payment/')



@login_required(login_url='customer-sign-in')
def customer_parking(request):
    customer=Customer.objects.get(user=request.user)
    price=0
    vehicle_type=None
    block=0
    table=TableOrder.objects.filter(customer=customer).last()
    food=FoodOrder.objects.filter(table=table)
    if request.method=='POST':
        parking_form=ParkingForm(request.POST)
        vehicle=request.POST.get('wheel')
        if parking_form.is_valid():
            vehicle_number=parking_form.cleaned_data.get('vehicle_number')
            if '2' in vehicle:
                price=150
                vehicle_type=vehicle
                block=random.randrange(200,300)
            elif '3' in vehicle:
                price=250
                vehicle_type=vehicle
                block=random.randrange(300,400)
            elif '4' in vehicle:
                price=400
                vehicle_type=vehicle
                block=random.randrange(400,500)
            parking=Parking(customer=customer,vehicle_type=vehicle_type,vehicle_number=vehicle_number,block=block,price=price)
            parking.save()
            for x in range(len(food)):
                foods=food[x].food
                food_order=FoodOrder(customer=customer,food=foods,table=table,checked=True,food_quantity=food[x].food_quantity,total_price=food[x].total_price,parking=parking)
                food_order.save()
                food_delete=FoodOrder.objects.get(id=food_order.id-1).delete()

                food_list=[foo.food.name for foo in food]
                food_quantity_list=[foo.food_quantity for foo in food]
                subject='Welcome to Restaurant'
                message='''
                Dear Mr.'''+request.user.username+'''\n
                Your Table is succesfully Booked with '''+'''
                Table No: '''+str(table.table_id)+''' of '''+str(table.table.seater)+''' seater
                on '''+str(table.date)+''' at '''+str(table.time)+''' time.
                with Food Items
                '''+str(food_list)+''' of quantity '''+str(food_quantity_list)+''' 
                and parking is also booked for '''+str(vehicle_type)+''' of vehicle 
                number '''+str(vehicle_number)+'''.
                The block number '''+str(block)+''' is reserved for your parking.
                Enjoy our delicious food .
                '''
                send_mail(subject,message,settings.EMAIL_HOST_USER,[request.user.email])
            return HttpResponseRedirect('/customer/payment/')
    else:  
        parking_form=ParkingForm()
    return render(request,'customer/parking.html',{'parkingform':parking_form})




@login_required(login_url='customer-sign-in')
def customer_view_parking(request,id):
    table=TableOrder.objects.get(id=id)
    customer=Customer.objects.get(user=request.user)
    food_order=FoodOrder.objects.filter(customer=customer).filter(table=table).last() 
    return render(request,'customer/viewparking.html',{'foodorder':food_order})

    
@login_required(login_url='customer-sign-in')
def customer_edit_parking(request,id):
    parking=Parking.objects.get(id=id)
    food_order=FoodOrder.objects.get(parking=parking)
    if request.method=='POST': 
        vehicle_type=request.POST.get('wheel')
        parking_form=ParkingForm(request.POST,instance=food_order.parking)
        if parking_form.is_valid():
            parking_form.save()
            food_order.parking.vehicle_type=vehicle_type
            food_order.save()
            return HttpResponseRedirect('/customer/tableacknowledgement/')
    else:
        parking_form=ParkingForm(instance=parking)
    return render(request,'customer/editparking.html',{'parkingform':parking_form})


@login_required(login_url='customer-sign-in')
def customer_delete_parking(request,id):
    parking=Parking.objects.get(id=id).delete()
    return HttpResponseRedirect('/customer/tableacknowledgement/')

@login_required(login_url='customer-sign-in')
def customer_payment(request):
    customer=Customer.objects.get(user=request.user)
    if request.method=='POST':
        return HttpResponseRedirect('/customer/tableacknowledgement/')
    total_price=0
    parking,table,foods=None,None,None
    global food_len
    food_lens=food_len
    food_order=FoodOrder.objects.last()
    if food_order.table:
        customer=Customer.objects.get(user=request.user)
        table=TableOrder.objects.filter(customer=customer).last() 
        foods=FoodOrder.objects.filter(table=table)
        if foods[len(foods)-1].parking:
            for food in foods:
                parking=food.parking
                total_price=total_price+food.total_price
            total_price=total_price+parking.price
        else:
            for food in foods:
                total_price=total_price+food.total_price
    elif food_order.address1:
        foods=FoodOrder.objects.filter(customer=customer).reverse()[0:food_lens]
        for food in foods:
            total_price=total_price+food.total_price
    return render(request,'customer/payment.html',{'table':table,'foods':foods,'total_price':total_price,'parking':parking})



@login_required(login_url='customer-sign-in')
def customer_edit_profile(request):
    customer=Customer.objects.get(user=request.user)
    user=User.objects.get(id=customer.user_id)
    if request.method=='POST':
        customer_update_form=CustomerUpdateForm(request.POST,request.FILES,instance=customer)
        user_update_form=UserUpdateForm(request.POST,instance=user)
        if customer_update_form.is_valid() and user_update_form.is_valid():
            user=user_update_form.save()
            customer=customer_update_form.save(commit=False)
            customer.user=user
            customer.save()
            return HttpResponseRedirect('/customer/payment/')
    else:
        customer_update_form=CustomerUpdateForm(instance=customer)
        user_update_form=UserUpdateForm(instance=user)
    return render(request,'customer/editprofile.html',{'userupdateform':user_update_form,'customerupdateform':customer_update_form,'customer':customer})




@login_required(login_url='customer-sign-in')
def customer_change_password(request):
    if request.method=='POST':
        password_form=PasswordChangeForm(user=request.user,data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request,password_form.user)
            return HttpResponseRedirect('/customer/profile/')
    else:
        password_form=PasswordChangeForm(user=request.user)
    return render(request,'customer/changepassword.html',{'passwordform':password_form})


    
@login_required(login_url='customer-sign-in')
def customer_logout(request):
    logout(request)
    return HttpResponseRedirect('/customer/signin/')