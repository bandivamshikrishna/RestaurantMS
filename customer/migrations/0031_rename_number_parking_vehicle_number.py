# Generated by Django 4.0.3 on 2022-05-20 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0030_parking_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parking',
            old_name='number',
            new_name='vehicle_number',
        ),
    ]
