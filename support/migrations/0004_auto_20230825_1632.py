# Generated by Django 3.2.20 on 2023-08-25 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_auto_20230822_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerquery',
            name='updated',
        ),
        migrations.AlterField(
            model_name='faq',
            name='published',
            field=models.BooleanField(default=True, help_text='Mark as published to make this FAQ visible on the site.'),
        ),
    ]
