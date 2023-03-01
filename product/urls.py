from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import api
from rest_framework_nested import routers
app_name='product'

router=DefaultRouter()
router.register('offers-manage',api.OfferView,basename='offers-manage')
router.register('idle-manage',api.IdleView,basename='idle-manage')
router.register('product-manage',api.ProductView,basename='product-manage')
router.register('company-manage',api.CompanyView,basename='company-manage')
router.register('cart',api.CartViewset,basename='cart')
router.register('ckeckout',api.Checkout,basename='checkout')
router.register('item', api.ItemListViewSet, basename='item')
#
item_router=routers.NestedDefaultRouter(router,'item',lookup="item")
item_router.register("offer",api.OfferItemViewSet,basename="item_offers")
#
#router.register('ret',api.RetrieveCart)
#router.register('del',api.DestroyCart)
cart_router=routers.NestedDefaultRouter(router,'cart',lookup="cart")
cart_router.register("items",api.CartItemViewSet,basename="cart_items")
#
urlpatterns = [
    path("",include(router.urls)),
    path("",include(cart_router.urls)),
    path("",include(item_router.urls)),
#
    path("companies",api.CompanyListView.as_view(),name='Companies'),
    path("idle",api.IdleListView.as_view(),name='idle'),
    path("offers",api.OfferListView.as_view(),name='offer list'),
    path("offers_store",api.StoreOfferListView.as_view(),name='store offers list'),

    #path("item",api.ItemListAPIView.as_view(),name='items list'),
    path("companies/products",api.products_campany,name='products of company'),
    path("checkout/<str:pk>",api.confirm_order,name='checkout'),
    path("itemoffer/<str:pk>",api.itemoffer,name='itemoffer'),

    path("finish/<str:pk>",api.finish_order,name='finish'),
    path("remove/<str:pk>",api.full_remove,name='remove items'),
    #path("itemoffer/<int:pk>",api.OfferItemViewSet.as_view(),name='offers items'),


]
