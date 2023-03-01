from django.shortcuts import render

# Create your views here.
class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer