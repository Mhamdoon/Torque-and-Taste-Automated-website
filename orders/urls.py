from django.urls import path
from . import views

urlpatterns = [
    path('orderlist/',views.order_list,name='order-list'),
    #make blank so that route url is blank which is the basic url
    path('update/<int:order_id>/', views.update_order_status, name='update-order-status')
    #When you click Update on order number 3, the browser needs to send a POST request to a URL that includes the order ID, like this:
     #/order/update/3/
    #The 3 is dynamic — 
    # it changes depending on which order you're updating.
    #  Django needs to capture that number from the URL and pass it to your view as order_id.
]