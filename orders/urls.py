from django.urls import path
from . import views

urlpatterns = [
    path('orderlist/',views.order_list,name='order-list')
    #make blank so that route url is blank which is the basic url
]