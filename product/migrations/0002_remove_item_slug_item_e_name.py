# Generated by Django 4.1.5 on 2023-02-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='slug',
        ),
        migrations.AddField(
            model_name='item',
            name='e_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
