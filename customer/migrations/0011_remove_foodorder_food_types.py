# Generated by Django 4.0.3 on 2022-05-14 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_foodorder_food_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodorder',
            name='food_types',
        ),
    ]
