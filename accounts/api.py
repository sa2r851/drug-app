from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view

# manager and admin
class DeliveryListView(generics.ListAPIView):
    queryset = DeliveryProfile.objects.all()
    serializer_class = DeliverySerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['country','city']
    search_fields = ['user']
# admin
class StoreListView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = Storelist_adminSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    #filterset_fields = ['country','city']
    search_fields = ['username']

# only admin

# manager and admin and delivery
class PharmaListView(generics.ListAPIView):
    queryset = Pharmacist.objects.all()
    serializer_class = PhManagerSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    #filterset_fields = ['country','city']
    search_fields = ['user']

class PharmacyRegistration(generics.CreateAPIView):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Pharmacy view his own profile
@api_view(['GET'])
def pharmacydetails(request):
    user =request.user
    details=PharmacistProfile.objects.get(user=user)
    data=Ph_Own_profileSerializer(details).data
    return Response({'data':data})
# Pharmacy Update his own profile

###############################
# Delivery view his own profile

# Delivery view profiles of pharmacies in his area
class Admin_PhListView(generics.ListAPIView):
    queryset = PharmacistProfile.objects.all()
    serializer_class = Ph_listSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['address',]
    filterset_fields = ['area']
# Delivery view profiles of store in his area
###################################
# Manager view his own profile
# Manager view profiles of pharmacies in his area
# Manager view profiles of store in his area
#######################################
# Admin view all profiles of pharmacies
class PhListView(generics.ListAPIView):
    queryset = PharmacistProfile.objects.all()
    serializer_class = Ph_listSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['user',]
    filterset_fields = ['area','country']
# Admin view all profiles of store
# Admin view all profiles of manager
class ManagerListView(generics.ListAPIView):
    queryset = Area_Manager.objects.all()
    serializer_class = ManagerSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['user']
# Admin view all profiles of delivery

# Admin Create new delivery
# Manager Create new delivery
class DeliveryRegistration(generics.CreateAPIView):
    queryset = Delivery_Agent.objects.all()
    serializer_class = DeliverySerializer

# Admin & Manager Create new pharmacy
class PharmacyRegistration(generics.CreateAPIView):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

# Admin Create new store
class StoreRegistration(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

# Admin Create new manager
class ManagerRegistration(generics.CreateAPIView):
    queryset = Area_Manager.objects.all()
    serializer_class = ManagerSerializer

class ManagerUpdateView(generics.UpdateAPIView):
    serializer_class = ManagerProfileSerializer
    def get_object(self):
        return Area_ManagerProfile.objects.get(user=self.request.user)

class PharmacyUpdateView(generics.UpdateAPIView):
    serializer_class = Ph_profileSerializer
    def get_object(self):
        return PharmacistProfile.objects.all()

