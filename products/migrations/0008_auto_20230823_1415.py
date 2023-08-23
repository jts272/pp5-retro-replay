# Generated by Django 3.2.20 on 2023-08-23 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='region',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='regions/'),
        ),
    ]