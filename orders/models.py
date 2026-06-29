from django.db import models

gender_choices = (
    ('male', 'Male'),
    ('female', 'Female'),
)

status_choices = (
    ('open', 'Open'),
    ('close', 'Close'),
)

payment_status_choices = (
    ('confirmed', 'Confirmed'),
    ('not_confirmed', 'Not Confirmed'),
)

order_status_choices = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('sent_to_kfc', 'Sent to KFC'),
    ('picked_up', 'Picked Up'),
    ('delivered', 'Delivered'),
)

class ServiceWindow(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices, default='open')
    def __str__(self):
     return self.status

class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, choices=gender_choices, default='female')

    def __str__(self):
        return self.name
    #so that it returns customer object as string without this it doesnt know the customer shows as Customer object (1) 
    # instead of the actual name. That's because Django doesn't know how to represent a Customer object as a string yet.

class MenuItem(models.Model):
    item_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
     return self.item_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_window = models.ForeignKey(ServiceWindow, on_delete=models.CASCADE)
    order_number = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='not_confirmed')
    order_status = models.CharField(max_length=15, choices=order_status_choices, default='pending')
    def __str__(self):
     return str(self.order_number)
    #order_number is an IntegerField — __str__ must return a string. Wrap it:

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
     return str(self.menu_item)
    #self.menu_item is a MenuItem object, not a string. But since Menu
    # Item already has a __str__ that returns item_name, just wrap it the same way:
