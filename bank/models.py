from django.db import models
from accounts.models import *
# Create your models here.


class Transaction(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='senderx')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    amount=models.FloatField(default=0.00)
    transaction_date = models.DateTimeField(auto_now=True, db_index=True)
    @property
    def transfer(self):
        if self.sender.balance > self.amount:
            self.receiver.balance = self.receiver.balance + self.amount
            self.sender.balance = self.sender.balance - self.amount

        else:
            print("No Balance")
        return self.receiver.balance
