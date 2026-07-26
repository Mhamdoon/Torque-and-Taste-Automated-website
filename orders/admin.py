from django.contrib import admin
from .models import ServiceWindow, Customer, Order, OrderItem, MenuItem

admin.site.register(ServiceWindow)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MenuItem)

# Register your models here.
