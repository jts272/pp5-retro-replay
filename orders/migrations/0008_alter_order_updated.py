# Generated by Django 3.2.20 on 2023-08-25 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_delivery_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Completed at'),
        ),
    ]
