from django.contrib import admin
from .models import Delivery, DeliveryAgent

# Register your models here.
admin.site.register(Delivery)
admin.site.register(DeliveryAgent)