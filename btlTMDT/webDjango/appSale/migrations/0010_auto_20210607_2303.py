# Generated by Django 3.1.7 on 2021-06-07 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appSale', '0009_salestaff_salecounter'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmOrder',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='saleStaff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appSale.salestaff'),
        ),
    ]
