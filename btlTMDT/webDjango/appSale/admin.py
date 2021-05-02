from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(ItemCart)
admin.site.register(Order)
# admin.site.register(Shipment)
# admin.site.register(Payment)
