from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class Pharmcyadmin(UserAdmin):
    pass
admin.site.register(User,Pharmcyadmin)
admin.site.register(Store)
admin.site.register(Area_Manager)
admin.site.register(Pharmacist)
admin.site.register(Delivery_Agent)
admin.site.register(DeliveryProfile)
admin.site.register(StoreProfile)
admin.site.register(Area_ManagerProfile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(PharmacistProfile)

