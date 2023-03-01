from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
from phonenumber_field.modelfields import PhoneNumberField
import random
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

# Create your models here.
#
SUPPLIER_CHOICES = [
    ('شركة', 'شركة'),
    ('مخزن', 'مخزن'),
]
class Area(models.IntegerChoices):
    FRIST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12
    THIRTEENTH = 13
    FOURTEENTH = 14
    FIFTEENTH = 15
    SIXTEENTH = 16
#
class Country(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
#
class City(models.Model):
    name=models.CharField(max_length=50)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
#
def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    if User.objects.filter(bank_id=key).exists():
        key = key_generator()
    return key
random_num =  random.randint(2345678909800, 9923456789000)
#
class User(AbstractUser):
    #bank_id=models.IntegerField(default=random_num,unique=True)
    class Role(models.TextChoices):
        ADMIN= 'ADMIN','Admin'
        AREA_MANAGER='AREA_MANAGER','Area_Manager'
        DELIVERY_AGENT='DELIVERY_AGENT',"Delivery_Agent"
        STORE='STORE','Store'
        PHARMACIST='PHARMACIST','Pharmacist'
    base_role=Role.ADMIN
    role = models.CharField(max_length=20,choices=Role.choices)
    balance=models.FloatField(default=0.00)
    def save(self,*args,**kwargs):
        if not self.pk:
            self.role=self.base_role
            return super().save(*args,**kwargs)
#
@receiver(post_save, sender=User)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
#
class Area_Manager_Manager(BaseUserManager):
    def get_queryset(self, *args,**kwargs):

        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.AREA_MANAGER)
#
class Area_Manager(User):
    base_role=User.Role.AREA_MANAGER
    store=Area_Manager_Manager()
    class Meta:
        proxy=True
#
class Area_ManagerProfile(models.Model):
    user = models.OneToOneField(Area_Manager, on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)  
#
@receiver(post_save, sender=Area_Manager)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "AREA_MANAGER":
        Area_ManagerProfile.objects.create(user=instance)
#
class StoreManager(BaseUserManager):
    def get_queryset(self, *args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.STORE)
#
class Store(User):
    base_role=User.Role.STORE
    objects=StoreManager()
    class Meta:
        proxy=True
#
class StoreProfile(models.Model):
    user = models.OneToOneField(Store, on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True, blank=True)
    address=models.TextField(max_length=200)
    phone_number = PhoneNumberField(blank=True)  
    supplier= models.CharField(max_length=20,choices=SUPPLIER_CHOICES)
    return_policy=models.TextField(max_length=400)

#
@receiver(post_save, sender=Store)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STORE":
        StoreProfile.objects.create(user=instance)
#
class PharmacistManager(BaseUserManager):
    def get_queryset(self, *args,**kwargs):
        password= make_password('password')

        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.PHARMACIST)
#
class Pharmacist(User):
    base_role=User.Role.PHARMACIST
    store=PharmacistManager()
    class Meta:
        proxy=True
#
class PharmacistProfile(models.Model):
    user = models.OneToOneField(Pharmacist, on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True, blank=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,null=True, blank=True)
    area = models.IntegerField(choices=Area.choices,null=True, blank=True)
    address=models.TextField(max_length=200)
    phone_number = PhoneNumberField(blank=True)
    def __str__(self):
        return str(self.user)
#
@receiver(post_save, sender=Pharmacist)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PHARMACIST":
        PharmacistProfile.objects.create(user=instance)
#
class Delivery_AgentManager(BaseUserManager):
    def get_queryset(self, *args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.DELIVERY_AGENT)
#
class Delivery_Agent(User):
    base_role=User.Role.DELIVERY_AGENT
    store=Delivery_AgentManager()
    class Meta:
        proxy=True
#
class DeliveryProfile(models.Model):
    user = models.OneToOneField(Delivery_Agent, on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.SET_NULL,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,null=True, blank=True)
    area = models.IntegerField(choices=Area.choices,null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)  
#
@receiver(post_save, sender=Delivery_Agent)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DELIVERY_AGENT":
        DeliveryProfile.objects.create(user=instance)
