from django.shortcuts import render
from django.http import HttpResponse
from .models import Order


def order_list(request):
    queryset = Order.objects.all()
    querysetpending=Order.objects.filter(order_status='pending').count()
    querysetconfirmed_count=Order.objects.filter(order_status='confirmed').count()
    querysetdelivered_count=Order.objects.filter(order_status='delivered').count()
# To retrieve all objects from a database table in Django, you use the all()
#  method on your model's default objects manager. This returns a QuerySet containing all database records as model instances
    return render(request,'orders/order_list.html',{'orders':queryset,'pending_count': querysetpending,'confirmed_count':querysetconfirmed_count,
    'delivered_count': querysetdelivered_count,})
#make my queryset available in the template under the name orders
#Queryset = the result of asking your database a question