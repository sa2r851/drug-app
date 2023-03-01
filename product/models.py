from django.db import models
from accounts.models import Store ,Pharmacist
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

SHAPE_CHOICES = [
    ('افلام', 'افلام'),
    ('اقراص', 'اقراص'),
    ('اكياس', 'اكياس'),
    ('امبولات', 'امبولات'),
    ('اسبراي', 'اسبراي'),
    ('اسبراي الانف', 'اسبراي الانف'),
    ('اسبراي الفم', 'اسبراي الفم'),
    ('اقراص استحلاب', 'اقراص استحلاب'),
    ('اقماع شرجية', 'اقماع شرجية'),
    ('اقماع مهبلية', 'اقماع مهبلية'),
    ('المحلول', 'المحلول'),
    ('برطمان', 'برطمان'),
    ('بلسم', 'بلسم'),
    ('بودرة', 'بودرة'),
    ('بودرة استنشاق', 'بودرة استنشاق'),
    ('جل', 'جل'),
    ('جل للعين', 'جل للعين'),
    ('جل مهبلي', 'جل مهبلي'),
    ('حبيبات فوارة', 'حبيبات فوارة'),
    ('حقنة معباة', 'حقنة معباه'),
    ('حليب مجفف', 'حليب مجفف'),
    ('خرطوشة', 'خرطوشة'),
    ('رغوة', 'رغوة'),
    ('زيت', 'زيت'),
    ('سائل', 'سائل'),
    ('شامبو', 'شامبو'),
    ('شراب', 'شراب'),
    ('صابون', 'صابون'),
    ('غسول للفم', 'غسول للفم'),
    ('غسول مهبلي', 'غسول مهبلي'),
    ('فيال', 'فيال'),
    ('قطرة انف', 'قطرة انف'),
    ('قطرة الاذن', 'قطرة الاذن'),
    ('قطرة للعين', 'قطرة للعين'),
    ('قطعة', 'قطعة'),
    ('قلم معبأ', 'قلم معبأ'),
    ('كبسولات', 'كبسولات'),
    ('كريم', 'كريم'),
    ('كريم مهبلي', 'كريم مهبلي'),
    ('لاصقات', 'لاصقات'),
    ('لوشن', 'لوشن'),
    ('لولب', 'لولب'),
    ('محلول استنشاق', 'محلول استنشاق'),
    ('محلول شرجي', 'محلول شرجي'),
    ('محلول وريدي', 'محلول وريدي'),
    ('مرهم', 'مرهم'),
    ('مرهم شرجي', 'مرهم شرجي'),
    ('مرهم للعين', 'مرهم للعين'),
    ('مستحلب', 'مستحلب'),
    ('معجون اسنان', 'معجون اسنان'),
    ('معلق', 'معلق'),
    ('نقط فم', 'نقط فم'),
]
#
LETTER_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z'),
]
#
class Company(models.Model):
    name=models.CharField(max_length=50,)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name
#
class Section(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name
#
class Item(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name=models.CharField(max_length=50)
    e_name = models.CharField(max_length=50)
    effective_material=models.CharField(max_length=100,default='المادة الفعالة')
    image=models.ImageField(blank = True, null=True, default='')
    puplic_price=models.FloatField(default=100.00)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    letter= models.CharField(max_length=20,choices=LETTER_CHOICES)
    shape= models.CharField(max_length=20,choices=SHAPE_CHOICES)
    def __str__(self):
        return self.name
#
class Offer(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name='offer')
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name='offer')
    precentage=models.FloatField(default=10)
    @property
    def price(self):
        new_price = self.item.puplic_price - ((self.precentage/100)*self.item.puplic_price)
        return new_price
#
class Idle(models.Model):
    pharmacy = models.ForeignKey(Pharmacist, on_delete=models.CASCADE,related_name='idle')
    product =  models.ForeignKey(Item, on_delete=models.CASCADE,related_name='idleitems')
    precentage=models.FloatField(default=10)
    stock=models.IntegerField(default=1)
    expire_data=models.DateField(blank=True,null=True)
#
class Take_Idle(models.Model):
    idle =  models.ForeignKey(Idle, on_delete=models.CASCADE,related_name='idleitems')
    needed = models.BooleanField(default=False)
    Pharmacy = models.ForeignKey(Pharmacist, on_delete=models.CASCADE,related_name='take_idle', null=True, default=None)
#
class Cart(models.Model):
    Pharmacy = models.ForeignKey(Pharmacist, on_delete=models.CASCADE,related_name='cart', null=True, default=None)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created=models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
#
@receiver(post_save, sender=Pharmacist)
def create_user_cart(sender, instance, created, **kwargs):
    if created and instance.role == "PHARMACIST":
        Cart.objects.create(Pharmacy=instance)
#
class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING,related_name='items')
    product =  models.ForeignKey(Offer, on_delete=models.CASCADE,related_name='carditems')
    quantity = models.PositiveSmallIntegerField(default=0)
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        if total == 0.00:
            self.delete()
        return total
    def __str__(self):
        return self.product.item.name
#
class Order(models.Model):
    Pharmacy = models.ForeignKey(Pharmacist, on_delete=models.CASCADE,related_name='order', null=True, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING,related_name='order')
    cartitems=models.ForeignKey(Cartitems, on_delete=models.PROTECT,related_name='order')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created=models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
