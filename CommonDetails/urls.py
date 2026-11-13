from django.urls import path
from . import views
from .views import *



urlpatterns = [
               
    path('brandlist/', views.fnGetBrands, name='fnGetBrands'),




]
