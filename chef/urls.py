from django.urls import path
from . import views


urlpatterns = [
    path('signup/',views.chef_sign_up,name='chef-sign-up'),
    path('signin/',views.chef_sign_in,name='chef-sign-in'),
    path('chefnotapproved/',views.chef_not_approved,name='chef-not-approved'),
    path('profile/',views.chef_profile,name='chef-profile'),
    path('foodorders/',views.chef_food_orders,name='chef-food-orders'),
    path('fooddeliveries/',views.chef_food_deliveries,name='chef-food-deliveries'),
    path('editprofile/',views.chef_edit_profile,name='chef-edit-profile'),
    path('changepassword/',views.chef_change_password,name='chef-change-password'),
    path('logout/',views.chef_logout,name='chef-logout'),
]
