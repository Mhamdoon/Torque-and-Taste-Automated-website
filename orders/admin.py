from django.contrib import admin
from .models import ServiceWindow
from .models import Customer
from .models import Order
from .models import OrderItem
from .models import MenuItem

admin.site.register(ServiceWindow)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MenuItem)

# Register your models here.
