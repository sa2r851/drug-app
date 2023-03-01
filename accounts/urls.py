from django.contrib import admin
from django.urls import path , include
from . import api
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name='accounts'
urlpatterns = [
    # Pharmacy
    path("pharmacy-profile/",api.pharmacydetails,name='Pharmacy profile'),
    path('updateprofile-pharm/', api.PharmacyUpdateView.as_view(), name='updateprofile-Pharmacy'),
    # Delivery
    path("pharm/",api.PharmaListView.as_view(),name='Pharmacies List'),
    path("manager/",api.ManagerListView.as_view(),name='Manager List'),
    path("store/",api.StoreListView.as_view(),name='Stores List'),
    path("delivery/",api.DeliveryListView.as_view(),name='Delivery List'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('register/', api.UserRegistration.as_view(), name='token_obtain_pair'),
    path('register-ph/', api.PharmacyRegistration.as_view(), name='Register-Pharmacy'),
    path('register-delivery/', api.DeliveryRegistration.as_view(), name='Register-Delivery'),
    path('register-store/', api.StoreRegistration.as_view(), name='Register-Store'),
    path('register-manager/', api.ManagerRegistration.as_view(), name='Register-Manager'),
    path('pharmcylist-manager/', api.PharmaListView.as_view(), name='Register-Manager'),
    path('storelist-manager/', api.StoreListView.as_view(), name='Register-Manager'),
    path('pharmacy-profile/', api.pharmacydetails, name='Register-Manager'),
    path('phlist-manager/', api.PhListView.as_view(), name='phlist-Manager'),
    path('phlist-manager/', api.PhListView.as_view(), name='phlist-Manager'),
    path('updateprofile-manager/', api.ManagerUpdateView.as_view(), name='updateprofile-Manager'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
