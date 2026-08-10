from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.shortcuts import redirect
from django.utils.timezone import now
from django.utils.timezone import now, localtime
from .models import ServiceWindow

def open_service_window(request):
    servicewindowstatuscheck=ServiceWindow.objects.filter(status='open').count()
    #checks to see if service window is open or not by gtetting the model and then finding the object where status is open and counting it
    if servicewindowstatuscheck == 0:
     #var to check status 
     Service_Window=ServiceWindow.objects.create(
     date =localtime(now()).date(),
     status='open'
     )
     #creating object of service window when its open
     return redirect('order-list')
    else:
       #creating object of service window when its open if its already oppen closing it and then opening a new one
       ServiceWindow.objects.filter(status='open').update(status='close')
       Service_Window=ServiceWindow.objects.create(
            date =localtime(now()).date(),
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
   context=get_dashboard_context(request)
  #method on your model's default objects manager. This returns a QuerySet containing all database records as model instances
   return render(request,'orders/order_list.html',context)

def kfc_rider_list(request):
   context=get_dashboard_context(request)
   confirmed_orders = Order.objects.filter(payment_status='confirmed', service_window=context['service_window'])
   #"Give me orders where service_window_id matches the ID of whichever ServiceWindow row currently has status='open'"
   print("DEBUG - confirmed orders found:", confirmed_orders)
   context['kfc_orders'] = confirmed_orders #adding a new dictionary with already added dictionaries into the mix
   return render(request,'orders/order_list.html',context)


#Each Django view runs independently with no memory of other views. 
#since kfc_order_list renders the same template as order_list, it needs the same base data (orders, pending_count, service_window, etc.) or the page breaks.
# it means it needs the same data as order list.
#Fix: pulled the shared queries into get_dashboard_context(request), which returns a dictionary. 
# Both views call it to get the base data, then add their own extra data on top — avoids duplicating queries in two places.
def get_dashboard_context(request):
   querysetorderwindow=ServiceWindow.objects.filter(status='open').first()
   queryset = Order.objects.filter(service_window=querysetorderwindow)
   #to show the data of only the current window
    # To retrieve all objects from a database table in Django, you use the all()
   querysetpending=Order.objects.filter(order_status='pending',service_window=querysetorderwindow).count()
   querysetconfirmed_count=Order.objects.filter(order_status='confirmed',service_window=querysetorderwindow).count()
   querysetdelivered_count=Order.objects.filter(order_status='delivered',service_window=querysetorderwindow).count()
   return {
        'orders': queryset,
        'pending_count': querysetpending,
        'confirmed_count': querysetconfirmed_count,
        'delivered_count': querysetdelivered_count,
        'service_window': querysetorderwindow,
    }
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

def confirm_payment(request,order_id):
   # order_id comes from the URL itself (e.g. /order/confirm-payment/3/)
    # Django's URL pattern captures it and hands it to this view automatically,
    # same mechanism you already used in update_order_status.
   order=Order.objects.get(id=order_id)
   # Fetches the ONE specific Order this button was clicked for.
   if request.method=='POST':
      if order.payment_status=='confirmed':
      # Update the field on the Order object IN MEMORY first.
      # Nothing is saved to the database yet at this point.  
       order.payment_status='not_confirmed'
       order.order_number = 0
      else:
         order.payment_status = 'confirmed'
         order.order_number=calculate_next_order_number(order.customer.gender,order.service_window)
             # THIS is the line that actually writes both changes (payment_status
               # AND order_number) to the PostgreSQL database. Until save() runs,
               # everything above only existed in Python's memory.
      order.save()
      return redirect('order-list')
   else:
      return redirect('order-list')


 
#views job is to calcualte and worry about the service window stuff and gender required . this ones only job is 
# to calculate the number 

def calculate_next_order_number(gender, service_window):
 if gender=='male':
    #checks for last male order by filtering it
    last_male_order = Order.objects.filter(
    service_window=service_window,
    customer__gender='male'
      ).order_by('-order_number').first()
    if last_male_order is None:
       next_number=1
       #default as 1
    else:
       next_number=last_male_order.order_number+1
       #take attribute of the last male order and add 1 
       if next_number % 10==9:
          #if it ends with 9 then skip and add 1 again 
          next_number+=1

   #The flow in one line: button click → POST request hits this view → 
   # view fetches the order → calculates the number using data already linked to that order → saves both changes at once → redirects.

 elif gender=='female':
    last_female_order = Order.objects.filter(
        service_window=service_window,
        customer__gender='female'
          ).order_by('-order_number').first()
    if last_female_order is None:
       next_number=9
    else:
       next_number=last_female_order.order_number+10
       #so gives 10 19 29 39 etc
    
 return next_number