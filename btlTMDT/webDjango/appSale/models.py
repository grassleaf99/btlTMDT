from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone = models.CharField(null=False, max_length=15)
    address = models.CharField(null=False, max_length=255)
    def __str__(self):
        return self.user.first_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    vitri = models.CharField(null=False, max_length=255)