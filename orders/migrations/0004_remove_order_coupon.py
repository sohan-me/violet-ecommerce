# Generated by Django 5.0.1 on 2025-03-01 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_city_order_country_order_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
    ]
