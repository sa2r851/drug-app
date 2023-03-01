from django.contrib import admin
from django.urls import path , include
from . import api

app_name='bank'
urlpatterns = [
    path("sakr",api.Moneyfollow,name='TRANSFER'),
    path("transfer",api.TransactionViewset.as_view({'post': 'create',}),name='transactions'),# 2

]
