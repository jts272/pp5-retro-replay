# Generated by Django 3.2.20 on 2023-08-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price paid at time of purchase', max_digits=6),
        ),
    ]
