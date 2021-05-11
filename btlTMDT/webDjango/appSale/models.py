from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    phone = models.CharField(null=False, max_length=15)
    address = models.CharField(null=False, max_length=255)
    def __str__(self):
        return self.user.first_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    vitri = models.CharField(null=False, max_length=255, blank=False)
    def __str__(self):
        return self.user.first_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) # khi xoa customer thi truong customer se duoc set thanh NULL
    date_order = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    def __str__(self):
        return str(self.id) + '_' + self.customer.user.first_name
    @property
    def get_cart_price(self):
        itemcarts = self.cart.itemcart_set.all()
        totalPrice = sum([itemcart.get_itemcart_price for itemcart in itemcarts])
        return totalPrice
    @property
    def get_cart_quantity(self):
        itemcarts = self.cart.itemcart_set.all()
        cartQuantity = sum([itemcart.quantity for itemcart in itemcarts])
        if cartQuantity != 0:
            return cartQuantity
        else:
            return 0

class Item(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.id) + '_' + 'order' + str(self.order.id)

class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id) + '_cart' + str(self.cart.id) + '_' + self.item.name + '_' + str(self.quantity)
    @property
    def get_itemcart_price(self):
        itemcartPrice = self.item.price * self.quantity
        return itemcartPrice
