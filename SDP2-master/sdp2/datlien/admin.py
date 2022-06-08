from django.contrib import admin
from .models import Account, Hub,State,CentralHub,City

# Register your models here.
class CentralHubAdmin(admin.ModelAdmin):
    list_display = ('state', 'city')

class HubAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'central_hub')

admin.site.register(State)
admin.site.register(Hub, HubAdmin)
admin.site.register(CentralHub, CentralHubAdmin)
admin.site.register(Account)
admin.site.register(City)