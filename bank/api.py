from .models import *
from .serializers import *
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin ,DestroyModelMixin ,ListModelMixin
from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from rest_framework.decorators import api_view
from accounts.models import User
from django.http import HttpResponseRedirect

class TransactionViewset(CreateModelMixin,GenericViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer


@api_view(['POST'])
def Moneyfollow(request):
    curr_user = MoneyTransfer.objects.get(sender=request.user)
    curr_user=User.username
    dest_user_acc_num = User.balance
    curr_user = User.objects.get(sender=request.user)
    dest_user = User.objects.get(balance=dest_user_acc_num)
    transfer_amount=MoneyTransfer.amount
    if curr_user.balance >= transfer_amount:
            curr_user.balance = curr_user.balance - transfer_amount
            dest_user.balance = dest_user.balance + transfer_amount
            # Save the changes before redirecting
            curr_user.save()
            dest_user.save()
    else:
        print('no baalance')

    return HttpResponseRedirect(redirect_to='https://google.com')
