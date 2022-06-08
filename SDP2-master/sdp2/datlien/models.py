from django.db import models
from django.contrib.auth.models import User
from django_random_id_model import RandomIDModel

# Create your models here.
class State(RandomIDModel):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class City(RandomIDModel):
    state = models.ForeignKey(State,on_delete=models.CASCADE,related_name='+')
    city = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.city} - {self.state}"

class CentralHub(RandomIDModel):
    state = models.ForeignKey(State,on_delete=models.CASCADE,related_name='+')
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='+')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    base_fare = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.city.city} - {self.state}"

class Hub(RandomIDModel):
    central_hub = models.ForeignKey(CentralHub,on_delete=models.CASCADE,related_name='+')
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='+')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    base_fare = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.city.city

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    role_choices = [
        ('1','SUPER USER'),
        ('2','CENTRAL HUB'),
        ('3','HUB'),
        ('4','DELIVERY MANAGER'),
        ('5','DELIVERY AGENT')
    ]
    role=models.CharField(max_length=1,choices=role_choices)
    def __str__(self):
        return self.user.get_username()

class DeliveryBoy(RandomIDModel):
    hub = models.ForeignKey(Hub,on_delete=models.CASCADE,related_name='+')
    gen = [
        ('M','Male'),
        ('F','Female')
    ]
    gender = models.CharField(max_length=1,choices=gen)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"