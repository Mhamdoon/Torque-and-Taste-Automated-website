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

class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, choices=gender_choices, default='female')

class MenuItem(models.Model):
    item_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_window = models.ForeignKey(ServiceWindow, on_delete=models.CASCADE)
    order_number = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='not_confirmed')
    order_status = models.CharField(max_length=15, choices=order_status_choices, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)