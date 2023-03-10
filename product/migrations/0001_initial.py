# Generated by Django 4.1.5 on 2023-03-07 19:18

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('is_received', models.BooleanField(default=False)),
                ('Pharmacy', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='accounts.pharmacist')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Idle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField(default=10)),
                ('stock', models.IntegerField(default=1)),
                ('expire_data', models.DateField(blank=True, null=True)),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idle', to='accounts.pharmacist')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('e_name', models.CharField(max_length=50)),
                ('effective_material', models.CharField(default='المادة الفعالة', max_length=100)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('public_price', models.FloatField(default=100.0)),
                ('letter', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=20)),
                ('shape', models.CharField(choices=[('افلام', 'افلام'), ('اقراص', 'اقراص'), ('اكياس', 'اكياس'), ('امبولات', 'امبولات'), ('اسبراي', 'اسبراي'), ('اسبراي الانف', 'اسبراي الانف'), ('اسبراي الفم', 'اسبراي الفم'), ('اقراص استحلاب', 'اقراص استحلاب'), ('اقماع شرجية', 'اقماع شرجية'), ('اقماع مهبلية', 'اقماع مهبلية'), ('المحلول', 'المحلول'), ('برطمان', 'برطمان'), ('بلسم', 'بلسم'), ('بودرة', 'بودرة'), ('بودرة استنشاق', 'بودرة استنشاق'), ('جل', 'جل'), ('جل للعين', 'جل للعين'), ('جل مهبلي', 'جل مهبلي'), ('حبيبات فوارة', 'حبيبات فوارة'), ('حقنة معباة', 'حقنة معباه'), ('حليب مجفف', 'حليب مجفف'), ('خرطوشة', 'خرطوشة'), ('رغوة', 'رغوة'), ('زيت', 'زيت'), ('سائل', 'سائل'), ('شامبو', 'شامبو'), ('شراب', 'شراب'), ('صابون', 'صابون'), ('غسول للفم', 'غسول للفم'), ('غسول مهبلي', 'غسول مهبلي'), ('فيال', 'فيال'), ('قطرة انف', 'قطرة انف'), ('قطرة الاذن', 'قطرة الاذن'), ('قطرة للعين', 'قطرة للعين'), ('قطعة', 'قطعة'), ('قلم معبأ', 'قلم معبأ'), ('كبسولات', 'كبسولات'), ('كريم', 'كريم'), ('كريم مهبلي', 'كريم مهبلي'), ('لاصقات', 'لاصقات'), ('لوشن', 'لوشن'), ('لولب', 'لولب'), ('محلول استنشاق', 'محلول استنشاق'), ('محلول شرجي', 'محلول شرجي'), ('محلول وريدي', 'محلول وريدي'), ('مرهم', 'مرهم'), ('مرهم شرجي', 'مرهم شرجي'), ('مرهم للعين', 'مرهم للعين'), ('مستحلب', 'مستحلب'), ('معجون اسنان', 'معجون اسنان'), ('معلق', 'معلق'), ('نقط فم', 'نقط فم')], max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.company')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Take_Idle',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('Pharmacy', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='take_idle', to='accounts.pharmacist')),
                ('idle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idleitems', to='product.idle')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_received', models.BooleanField(default=False)),
                ('Pharmacy', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='accounts.pharmacist')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='product.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField(default=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='product.item')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='accounts.store')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.section'),
        ),
        migrations.AddField(
            model_name='idle',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idleitems', to='product.item'),
        ),
        migrations.CreateModel(
            name='Cartitems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='product.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carditems', to='product.offer')),
            ],
        ),
    ]
