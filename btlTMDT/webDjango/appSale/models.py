from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Fullname(models.Model):
    firstName = models.CharField(null=False, blank=False, max_length=255)
    midName = models.CharField(null=True, blank=True, max_length=255)
    lastName = models.CharField(null=False, blank=False, max_length=255)
    def __str__(self):
        return 'Name of ' + self.customer.user.username

class Address(models.Model):
    houseNum = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    def __str__(self):
        return 'Address of ' + self.customer.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    fullname = models.OneToOneField(Fullname, on_delete=models.CASCADE, null=False, blank=False, default=None)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=False, blank=False)
    phone = models.CharField(null=False, blank=False, max_length=15)
    email = models.CharField(null=False, blank=False, max_length=255, default='bua@gmail.com')
    def __str__(self):
        return self.fullname.firstName


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return self.user.username


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    vitri = models.CharField(null=False, max_length=255, blank=False)
    salary = models.FloatField(default=0.0)
    def __str__(self):
        return self.user.username


class WarehouseStaff(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return self.employee.user.username


class BusinessStaff(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return self.employee.user.username


class SaleStaff(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, blank=False)
    saleCounter = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.employee.user.username


class Payment(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    desc = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) # khi xoa customer thi truong customer se duoc set thanh NULL
    saleStaff = models.ForeignKey(SaleStaff, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    confirmOrder = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        if self.customer == None:
            return str(self.id)
        #return str(self.id) + '_' + self.customer.fullname.firstName
        return str(self.pk) + '_' + self.customer.fullname.firstName
    @property
    def shipPrice(self):
        return 1.0
    @property
    def totalOrderPrice(self):
        return self.cart.get_cart_price + self.shipPrice


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    desc = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # khi xoa category thi truong category se duoc set thanh NULL
    price = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def imgUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Cart(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.id) + '_' + 'order' + str(self.order.id)
    @property
    def get_cart_price(self):
        itemcarts = self.itemcart_set.all()
        totalPrice = sum([itemcart.get_itemcart_price for itemcart in itemcarts])
        return totalPrice
    @property
    def get_cart_quantity(self):
        itemcarts = self.itemcart_set.all()
        cartQuantity = sum([itemcart.quantity for itemcart in itemcarts])
        if cartQuantity != 0:
            return cartQuantity
        else:
            return 0


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
