from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer
#
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
#
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields =fields = "__all__"
#
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields =fields = "__all__"
#
class IcitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields =fields = ['name']
#
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProfile
        fields =fields = "__all__"
#
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields =fields = "__all_"
#
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area_ManagerProfile
        fields =fields = "__all_"
#
class Mycreate(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields=['username','password','id','role']
#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields=['username','password','role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class PharmacistSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="PHARMACIST")
    class Meta:
        model = Pharmacist
        fields=['username','password','role']

    def create(self, validated_data):
        user = Pharmacist(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class DeliverySerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="DELIVERY_AGENT")

    class Meta:
        model = Delivery_Agent
        fields=['username','password','role']

    def create(self, validated_data):
        user = Delivery_Agent(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class StoreSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="STORE")
    class Meta:
        model = Store
        fields=['username','password','role']

    def create(self, validated_data):
        user = Store(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class ManagerSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="AREA_MANAGER")
    class Meta:
        model = Area_Manager
        fields=['username','password','role']
    def create(self, validated_data):
        user = Area_Manager(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class PhManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields =['username']
#
class Storelist_adminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields =['id','username']
#
class SimplePharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields=['username','balance']
#
class PhSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields=['username']
#
class Ph_listSerializer(serializers.ModelSerializer):
    user=PhSimpleSerializer()
    class Meta:
        model = PharmacistProfile
        fields = ['pk','user','area']
#
class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area_ManagerProfile
        fields = ['pk','user','country','phone_number']
        read_only_fields = ('user', 'country')
#
class Ph_profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = ['pk','user','address','country','city','area','phone_number']
#
class SimpleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields =fields = ['username']
#
class Ph_Own_profileSerializer(serializers.ModelSerializer):
    user=SimplePharmacistSerializer(many=False)
    country=CountrySerializer(many=False)
    city=IcitySerializer(many=False)
    class Meta:
        model = PharmacistProfile
        fields = ['pk','user','address','country','city','area','phone_number']