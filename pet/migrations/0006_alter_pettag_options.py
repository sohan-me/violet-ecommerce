# Generated by Django 5.0.1 on 2025-03-27 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0005_remove_pettag_dob_pettag_age'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pettag',
            options={'verbose_name': 'Pet', 'verbose_name_plural': 'Pets'},
        ),
    ]
