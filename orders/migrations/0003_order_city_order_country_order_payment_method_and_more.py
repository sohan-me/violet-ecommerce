# Generated by Django 5.0.1 on 2025-03-01 10:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_is_ordered_orderproduct_ordered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=django.utils.timezone.now, max_length=55),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='post_code',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
