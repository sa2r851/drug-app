from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Company)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Offer)
admin.site.register(Idle)
admin.site.register(Section)
admin.site.register(Order)
admin.site.register(Take_Idle)


