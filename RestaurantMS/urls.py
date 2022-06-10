"""RestaurantMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('review/',views.review,name='review'),
    path('menu/',views.menu,name='menu'),
    path('tablebooking/',views.table_booking,name='tablebooking'),
    path('afterlogin/',views.afterlogin,name='afterlogin'),
    path('jsiq87/',JavaScriptCatalog.as_view(),name='js-catalog'),


    path('customer/',include('customer.urls')),
    path('chef/',include('chef.urls')),


    path('admin-signin/',views.admin_sign_in,name='admin-sign-in'),
    path('admin-add-table/',views.admin_add_table,name='admin-add-table'),
    path('admin-add-food/',views.admin_add_food,name='admin-add-food'),
    path('admin-table-orders/',views.admin_table_orders,name='admin-table-orders'),
    path('admin-food-orders/',views.admin_food_orders,name='admin-food-orders'),
    path('admin-food-deliveries/',views.admin_food_deliveries,name='admin-food-deliveries'),
    path('admin-approved-chef/',views.admin_approved_chef,name='admin-approved-chef'),
    path('admin-approving-chef/<int:id>/',views.admin_approving_chef,name='admin-approving-chef'),
    path('admin-rejecting-chef/<int:id>/',views.admin_rejecting_chef,name='admin-rejecting-chef'),
    path('admin-pending-chef/',views.admin_pending_chef,name='admin-pending-chef'),
    path('admin-parking-details/',views.admin_parking_details,name='admin-parking-details'),
    path('admin-logout/',views.admin_logout,name='admin-logout'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
