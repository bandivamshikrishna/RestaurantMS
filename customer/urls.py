from django.urls import path
from . import views


urlpatterns = [

    #customer specific urls
    path('signup/',views.customer_sign_up,name='customer-sign-up'),
    path('signin/',views.customer_sign_in,name='customer-sign-in'),
    path('dashboard/',views.customer_dashboard,name='customer-dashboard'),
    path('profile/',views.customer_profile,name='customer-profile'),
    path('editprofile/',views.customer_edit_profile,name='customer-edit-profile'),
    path('changepassword/',views.customer_change_password,name='customer-change-password'),
    path('logout/',views.customer_logout,name='customer-logout'),

    

    path('fooddelivery/',views.customer_food_delivery,name='customer-food-delivery'),
    path('fooddeliveryedit/<int:id>/',views.customer_food_delivery_edit,name='customer-food-delivery-edit'),
    path('fooddeliverydelete/<int:id>/',views.customer_food_delivery_delete,name='customer-food-delivery-delete'),
    
    
    #Table specific urls
    path('reservetable/',views.customer_reserve_table,name='customer-reserve-table'),
    path('tableorder/<int:id>/',views.customer_table_order,name='customer-table-order'),
    path('menuyesorno/',views.customer_menu_yes_or_no,name='customer-menu-or-no'),
    path('tablebookedmail/',views.table_booked_mail,name='customer-table-booked-mail'),
    path('tableacknowledgement/',views.customer_table_acknowledgement,name='customer-table-acknowledgement'),
    path('tableedit/<int:id>/',views.customer_table_edit,name='customer-table-edit'),
    path('tablecancel/<int:id>/',views.customer_table_cancel,name='customer-table-cancel'),
    
    path('reservefood/',views.customer_reserve_food,name='customer-reserve-food'),  
    path('foodacknowledgement/<int:id>/',views.customer_food_acknowledgement,name='customer-food-acknowledgement'),  
    path('foodedit/<int:id>/',views.customer_food_edit,name='customer-food-edit'),
    path('foodcancel/<int:id>/',views.customer_food_cancel,name='customer-food-cancel'),


    path('parkingyesorno/',views.customer_parking_yes_or_no,name='customer-parking-or-no'),
    path('tablefoodbookedmail/',views.table_food_booked_mail,name='customer-table-food-booked-mail'),
    path('parking/',views.customer_parking,name='customer-parking'),
    path('viewparking/<int:id>/',views.customer_view_parking,name='customer-view-parking'),
    path('editparking/<int:id>/',views.customer_edit_parking,name='customer-edit-parking'),
    path('deleteparking/<int:id>/',views.customer_delete_parking,name='customer-delete-parking'),
    path('payment/',views.customer_payment,name='customer-payment'),
    
]
