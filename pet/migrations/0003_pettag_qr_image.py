# Generated by Django 5.0.1 on 2025-03-25 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0002_pettag_qr_code_alter_pettag_breed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pettag',
            name='qr_image',
            field=models.ImageField(blank=True, null=True, upload_to='pets/qrcodes/'),
        ),
    ]
