from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.shortcuts import redirect
from django.utils.timezone import now
from .models import ServiceWindow

def open_service_window(request):
    servicewindowstatuscheck=ServiceWindow.objects.filter(status='open').count()
    #checks to see if service window is open or not by gtetting the model and then finding the object where status is open and counting it
    if servicewindowstatuscheck == 0:
     #var to check status 
     Service_Window=ServiceWindow.objects.create(
     date = now().date(),
     status='open'
     )
     #creating object of service window when its open
     return redirect('order-list')
    else:
       #creating object of service window when its open if its already oppen closing it and then opening a new one
       ServiceWindow.objects.filter(status='open').update(status='close')
       Service_Window=ServiceWindow.objects.create(
            date = now().date(),
            status='open'
            )
       return redirect('order-list')

       


#open_service_window checks if a window is open at the moment someone
#  clicks the button — it's a one-time check used to decide whether
#  to create a new window or close-then-create.
#But order_list is a completely different view — it's the one that runs every time the 
# dashboard page loads. It needs to know "is there currently an open service window?" so it can:
#Show the correct badge (Service Open vs Service Closed)
#Show the correct button text (Open New Service vs already running)
#open_service_window → runs ONCE, when the admin clicks the button
#order_list → runs EVERY TIME the dashboard page loads/refreshes
def order_list(request):
    querysetorderwindow=ServiceWindow.objects.filter(status='open').first()
    queryset = Order.objects.all()
    querysetpending=Order.objects.filter(order_status='pending').count()
    querysetconfirmed_count=Order.objects.filter(order_status='confirmed').count()
    querysetdelivered_count=Order.objects.filter(order_status='delivered').count()
# To retrieve all objects from a database table in Django, you use the all()
#  method on your model's default objects manager. This returns a QuerySet containing all database records as model instances
    return render(request,'orders/order_list.html',{'orders':queryset,'pending_count': querysetpending,'confirmed_count':querysetconfirmed_count,
    'delivered_count': querysetdelivered_count,'service_window':querysetorderwindow})
#make my queryset available in the template under the name orders
#Queryset = the result of asking your database a question


#def update_order_status(request, order_id):
#  get the order from database using order_id
#if request is POST:
#  get the new status from the form data
# set order.order_status to new status
# save the order
# redirect to order list
def update_order_status(request,order_id):
    order=Order.objects.get(id=order_id)
    if request.method=='POST':
        new_status = request.POST.get('order_status') #the thing user posts
        order.order_status = new_status
        order.save()
        return redirect('order-list')
    else:
       new_status=order.order_status
       return redirect('order-list')
#When Django finishes updating the order, 
# it needs to send the user somewhere. Without a redirect, the page would just be blank after the update.
#In simple terms — update happens → redirect → user sees the refreshed dashboard with the new status showing.




#full flow is Template renders order.id into the URL → 
#form action = /order/update/3/ → 
#user clicks submit → 
#POST request goes to /order/update/3/ → 
#Django captures 3 as order_id → 
#view fetches that order → 
#updates its status → 
#redirects back