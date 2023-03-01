from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics ,viewsets,mixins
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerPharmacy , IsOwnerStore
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin ,DestroyModelMixin
from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from accounts.models import PharmacistProfile,Pharmacist
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

#
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name']
    authentication_classes = [TokenAuthentication]
    pagination_class=PageNumberPagination
    # permission_classes = [IsAuthenticated]

# منتجات الشركة
@api_view(['GET'])
def products_campany(request):
    details=Item.objects.filter(Company=Company.company_id)
    data=ItemSerializer(details,many=True).data
    return Response({'data':data})
# قائمة الاقسام الرئيسية
@api_view(['GET'])
def products_campany(request):
    details=Offer.objects.filter(Company=Company.company_id)
    data=OfferSerializer(details,many=True).data
    return Response({'data':data})
# pharmacy and store
class ItemListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','e_name','effective_material']
    filterset_fields = ['shape','letter','company']
    lookup_field = "id"

    #authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
#only owner Pharmacy

# pharmacy

# pharmacy
class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['item__name','item__e_name','item__effective_material']
    filterset_fields = ['item__shape','item__letter','item__company','item__section']
    #authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

#only stores
class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class RetrieveCart(RetrieveModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class DestroyCart(DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ckeckout(APIView):
    serializer_class=CartSerializer
    def post(request, pk):
        user =request.user
        cart = Cart.objects.get(id=pk,Pharmacy=user,completed=False)
        cart.completed = True
        cart.save()
        messages.success(request, "تم ارسال طلبك")
        Cart.objects.create(Pharmacy=request.user)
        return HttpResponseRedirect(redirect_to='https://google.com')

class OrderListView(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(Pharmacy=user,completed=True,is_received=False)
    serializer_class = CartSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerPharmacy]

# Pharmacy manage (add & edit & delete) his cart
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','delete','patch']
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddCartItemSerializer
        elif self.request.method=="PATCH":
            return UpdateCartitemSerializer
        return CartitemSerializer
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

# Pharmacy manage (add & edit & delete) his idle
class IdleView(viewsets.ModelViewSet):
    serializer_class = IdleSerializer
    def get_queryset(self):
        user = self.request.user

        return Idle.objects.filter(pharmacy=user)
# Pharmacy view his previous orders
@api_view(['GET'])
def previous_orders(request):
    details=Cart.objects.filter(Pharmacy=request.user,completed=True,is_received=True)
    data=CartSerializer(details,many=True).data
    return Response({'data':data})
# Pharmacy view his in progress orders
@api_view(['GET'])
def in_progress_orders(request):
    details=Cart.objects.filter(Pharmacy=request.user,completed=True,is_received=False)
    data=CartSerializer(details,many=True).data
    return Response({'data':data})
# Pharmacy view all idle in his area
class IdleListView(generics.ListAPIView):
    serializer_class = IdleListSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['product__name','product__e_name','product__effective_material']
    filterset_fields = ['product__shape','product__letter','product__company']
    def get_queryset(self):
        return Idle.objects.all()

# Pharmacy view  idle details
# Pharmacy take idle
@api_view(['POST'])
def idle(request, pk):
    user =request.user
    cart = Take_Idle.objects.get(id=pk,Pharmacy=user,needed=False)
    cart.needed = True
    cart.save()
    messages.success(request, "تم ارسال طلبك")
    return HttpResponseRedirect(redirect_to='https://google.com')
# Pharmacy checkout
@api_view(['POST'])
def confirm_order(request, pk):
    user =request.user
    cart = Cart.objects.get(id=pk,Pharmacy=user,completed=False)
    cart.completed = True
    cart.save()
    messages.success(request, "تم ارسال طلبك")
    Cart.objects.create(Pharmacy=request.user)
    return HttpResponseRedirect(redirect_to='https://google.com')

#######################################################
# Store manage (add & edit & delete) his offers
class OfferView(CreateModelMixin,GenericViewSet):
    serializer_class = ItemOfferSerializer
    def get_queryset(self):
        user=self.request.user
        return Offer.objects.filter(store=user)
########################################################
# Delivery view all previous orders in his area
# Delivery view all in progress orders in his area
########################################################
# Manager view all previous orders in his area
# Manager view all in progress orders in his area
##########################################################
# Admin view all previous orders
@api_view(['GET'])
def all_previous_orders(request):
    details=Cart.objects.filter(completed=True,is_received=True)
    data=CartSerializer(details,many=True).data
    return Response({'data':data})

# Admin view all in progress orders
@api_view(['GET'])
def all_in_progress_orders(request):
    details=Cart.objects.filter(completed=True,is_received=True)
    data=CartSerializer(details,many=True).data
    return Response({'data':data})

# Admin & Manager & Delivery finish orders
@api_view(['POST'])
def finish_order(request, pk):
    cart = Cart.objects.get(id=pk,completed=True,is_received=False)
    cart.is_received = True
    cart.save()
    messages.success(request, "Done")
    return HttpResponseRedirect(redirect_to='https://google.com')

# Admin & manager manage (add & edit & delete) products
class ProductView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = CreateItemSerializer



# Admin & manager manage (add & edit & delete) company
class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

# Admin view all idle
class AllIdleListView(generics.ListAPIView):
    queryset = Idle.objects.all()
    serializer_class = IdleSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['product__name','product__e_name','product__effective_material']
    filterset_fields = ['product__shape','product__letter','product__company','pharmacy__country']

class Checkout(CreateModelMixin,GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self    #user=SimplePharmacistSerializer(many=False)
    #country=CountrySerializer(many=False)
    #city=IcitySerializer(many=False)
,request,pk, *args, **kwargs):
        queryset = [
            {'queryset': Cart.objects.get(id=pk),
             'serializer_class': CartSerializer},
            {'queryset': Cartitems.objects.filter(card=pk),
             'serializer_class': CartitemSerializer}
        ]
        return queryset


@api_view(['POST'])
def full_remove(request,pk):
     cart = Cart.objects.get(id=pk)
     cart_items = Cartitems.objects.filter(cart=cart)
     cart_items.delete()
     return HttpResponseRedirect(redirect_to='https://google.com')



'''
class JlistView(ObjectMultipleModelAPIView):
    queryset = Jlist.objects.all()

    def get_queryset(self, *args, **kwargs):
        userId = self.kwargs.get('pk')
        queryset = [
            {'queryset': Jlist.objects.all(),
             'serializer_class': JlistSerializers},
            {'queryset': JStarList.objects.filter(userId=userId),
             'serializer_class': JStarList}
        ]
        return queryset
'''
@api_view(['GET'])
def offers_store(self,request):
    user=self.request.user
    details=Offer.objects.filter(store=user)
    data=OfferSerializer(details,many=True).data
    return Response({'data':data})

class StoreOfferListView(generics.ListAPIView):
    serializer_class = OfferSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['item__name','item__e_name','item__effective_material']
    filterset_fields = ['item__shape','item__letter','item__company']
    def get_queryset(self):
        user=self.request.user
        return Offer.objects.filter(store=user)
#
class OfferItemViewSet(ModelViewSet):
    http_method_names=['get',]
    def get_queryset(self):
        return Offer.objects.filter(item=self.kwargs["item_pk"])
    def get_serializer_class(self):
        if self.request.method=="GET":
            return OfferDetailSerializer
    def get_serializer_context(self):
        return {"item_id": self.kwargs["item_pk"]}

@api_view(['GET'])
def itemoffer(request,id):
    details=Item.objects.get(id=id)
    data=ItemOfferSerializer(details).data
    return Response({'data':data})
