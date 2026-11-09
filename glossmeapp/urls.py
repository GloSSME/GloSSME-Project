from django.urls import path
from . import views
from .views import *



urlpatterns = [
                path('commonvalues/',views.fnCommonValues,name='fnCommonValues'),
                
    
    path('verifyregisteredmembers/',views.fnVerifyRegisteredMembers,name='VeryfyRegisteredMembers'),
    path('verifypreviousinstallation/',views.fnVerifyPreviousInstallation,name='VerifyPreviousInstalltion'),
    path('deviceinstallupdate/', views.fnDeviceInstallUpdate,name='fnDeviceInstallUpdate'),         #   Mobileapp

    
    
    
    path('adduser/',views.fnAddUser,name='fnAddUser'),

    path('addservice/',views.fnSaveService,name='fnSaveService'),




]
