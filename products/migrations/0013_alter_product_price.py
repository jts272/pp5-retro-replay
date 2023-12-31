# Generated by Django 3.2.20 on 2023-08-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Please enter the price in decimal format, e.g. 9.99', max_digits=6),
        ),
    ]
