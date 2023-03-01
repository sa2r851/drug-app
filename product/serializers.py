from rest_framework import serializers
from .models import *
from accounts.serializers import SimplePharmacistSerializer ,SimpleStoreSerializer
#
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
#
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
#
class ItemSerializer(serializers.ModelSerializer):
    company=CompanySerializer()
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','puplic_price','company']
#
class IdleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    #pharmacy=SimplePharmacistSerializer()
    #product=ItemSerializer()
    class Meta:
        model = Idle
        fields = ['id','pharmacy','product','precentage','stock','expire_data']
#
class OfferSerializer(serializers.ModelSerializer):
    item=ItemSerializer()
    store=SimpleStoreSerializer()
    class Meta:
        model = Offer
        fields =['item','store','precentage','price']
###
class ItemOfferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields =['id','item','store','precentage','price']
        #read_only_fields = ('store',)
###
class CartitemSerializer(serializers.ModelSerializer):
    product=OfferSerializer()
    sub_total=serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = Cartitems
        fields =['id','cart','product','quantity','sub_total']
    def total(self,cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price
#
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    items=CartitemSerializer(many=True)
    grand_total=serializers.SerializerMethodField(method_name="main_total")
    class Meta:
        model = Cart
        fields =['id','items','grand_total']
    def main_total(self,cart:Cart):
        items=cart.items.all()
        total=sum([item.quantity * item.product.price  for item in items])
        return total
#
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    #
    def validate_product_id(self, value):
        if not Offer.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    #
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        #
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
        
    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]
#
class UpdateCartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields =['quantity']
#
class OrderSerializer(serializers.ModelSerializer):
    #cart=CartSerializer(many=False)
    #id = serializers.UUIDField()
    class Meta:
        model = Order
        fields =['Pharmacy','cart','created','is_received','cartitems']
#
class IdleListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    #pharmacy=SimplePharmacistSerializer()
    product=ItemSerializer()

    class Meta:
        model = Idle
        fields = ['id','pharmacy','product','precentage','stock','expire_data']
#
class CreateItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','puplic_price','company','section','letter','shape','e_name']




class OfferDetailSerializer(serializers.ModelSerializer):
    store=SimpleStoreSerializer()
    class Meta:
        model = Offer
        fields=['precentage','price','store','id']

class ItemOfferSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    offer=OfferDetailSerializer(many=True)
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','puplic_price','company','offer']
